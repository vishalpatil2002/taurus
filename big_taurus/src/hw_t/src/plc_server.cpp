#include <ros/ros.h>
#include <actionlib/server/simple_action_server.h>
#include "hw_t/ConveyorAction.h"

#include <modbus/modbus.h>
#include <cerrno>

class ConveyorActionServer
{
private:
    ros::NodeHandle nh_;
    actionlib::SimpleActionServer<hw_t::ConveyorAction> as_;

    hw_t::ConveyorFeedback feedback_;
    hw_t::ConveyorResult result_;

    modbus_t* ctx_;

    std::string plc_ip_;
    int plc_port_;

    ros::Timer watchdog_timer_;

public:

    ConveyorActionServer() :
        as_(nh_, "conveyor_action",
            boost::bind(&ConveyorActionServer::executeCB, this, _1),
            false),
        ctx_(nullptr)
    {
        nh_.param("plc_ip", plc_ip_, std::string("192.168.7.5"));
        nh_.param("plc_port", plc_port_, 502);

        ctx_ = connect_modbus();

        watchdog_timer_ = nh_.createTimer(
            ros::Duration(2.0),
            &ConveyorActionServer::watchdogCB,
            this);

        as_.start();
        ROS_INFO("Conveyor Action Server Ready");
    }

    ~ConveyorActionServer()
    {
        if (ctx_)
        {
            modbus_close(ctx_);
            modbus_free(ctx_);
        }
    }

    modbus_t* connect_modbus()
    {
        while (ros::ok())
        {
            modbus_t* c = modbus_new_tcp(plc_ip_.c_str(), plc_port_);

            if (!c)
            {
                ROS_ERROR("Failed to create Modbus context");
                ros::Duration(2.0).sleep();
                continue;
            }

            if (modbus_connect(c) == -1)
            {
                ROS_ERROR("Modbus connect failed: %s",
                          modbus_strerror(errno));
                modbus_free(c);
                ros::Duration(2.0).sleep();
                continue;
            }

            ROS_INFO("Modbus connected to %s:%d",
                     plc_ip_.c_str(), plc_port_);

            return c;
        }
        return nullptr;
    }

    void reconnect()
    {
        ROS_WARN("Reconnecting to PLC...");

        if (ctx_)
        {
            modbus_close(ctx_);
            modbus_free(ctx_);
        }

        ctx_ = connect_modbus();
    }

    bool write_coil(int coil)
    {
        if (!ctx_) return false;

        if (modbus_write_bit(ctx_, coil, 1) == -1)
        {
            ROS_ERROR("Write failed: %s",
                      modbus_strerror(errno));
            reconnect();
            return false;
        }

        return true;
    }

    bool read_coil(int coil)
    {
        uint8_t status;

        if (!ctx_) return false;

        if (modbus_read_bits(ctx_, coil, 1, &status) == -1)
        {
            ROS_ERROR("Read failed: %s",
                      modbus_strerror(errno));
            reconnect();
            return false;
        }

        return status;
    }

    void stop()
    {
        write_coil(9);  // STOP coil
    }

    void watchdogCB(const ros::TimerEvent&)
    {
        if (!ctx_)
        {
            reconnect();
            return;
        }

        uint8_t status;
        if (modbus_read_bits(ctx_, 0, 1, &status) == -1)
        {
            ROS_ERROR("Watchdog lost connection");
            reconnect();
        }
    }

    void executeCB(const hw_t::ConveyorGoalConstPtr &goal)
    {
        if (!ctx_)
        {
            result_.success = false;
            result_.message = "PLC not connected";
            as_.setAborted(result_);
            return;
        }

        if (as_.isPreemptRequested())
        {
            stop();
            as_.setPreempted();
            return;
        }

        int coil = -1;

        if (goal->mode == 0) coil = 9;   // STOP
        if (goal->mode == 1) coil = 7;   // FORWARD
        if (goal->mode == 2) coil = 8;   // BACKWARD

        if (coil == -1)
        {
            result_.success = false;
            result_.message = "Invalid mode";
            as_.setAborted(result_);
            return;
        }

        // For FORWARD and BACKWARD, send STOP first before motion command
        if (goal->mode == 1 || goal->mode == 2)
        {
            ROS_INFO("Sending pre-stop before motion command...");

            if (!write_coil(9))
            {
                result_.success = false;
                result_.message = "Pre-stop write failed";
                as_.setAborted(result_);
                return;
            }

            ros::Duration(0.5).sleep();  // small delay for PLC to process stop
        }

        if (!write_coil(coil))
        {
            result_.success = false;
            result_.message = "Write failed";
            as_.setAborted(result_);
            return;
        }

        // Wait for PLC confirmation
        ros::Rate rate(5);

        for (int i = 0; i < 20; i++)  // wait 4 sec
        {
            if (as_.isPreemptRequested())
            {
                stop();
                as_.setPreempted();
                return;
            }

            bool status = read_coil(coil);

            feedback_.current_state = status;
            as_.publishFeedback(feedback_);

            if (status)
            {
                result_.success = true;
                result_.message = "Command Executed Successfully";
                as_.setSucceeded(result_);
                return;
            }

            rate.sleep();
        }

        result_.success = false;
        result_.message = "PLC did not confirm action";
        as_.setAborted(result_);
    }
};

int main(int argc, char **argv)
{
    ros::init(argc, argv, "plc_server");
    ConveyorActionServer server;
    ros::spin();
    return 0;
}