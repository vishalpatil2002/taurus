#include <ros/ros.h>
#include <actionlib/server/simple_action_server.h>
#include "hw_t/ConveyorAction.h"
#include "conveyor_control.h"

class ConveyorActionServer
{
private:
    ros::NodeHandle nh_;
    actionlib::SimpleActionServer<hw_t::ConveyorAction> as_;
    std::string action_name_;

    hw_t::ConveyorFeedback feedback_;
    hw_t::ConveyorResult result_;

    ConveyorControl conveyor_;

public:
    ConveyorActionServer(std::string name) :
        as_(nh_, name, boost::bind(&ConveyorActionServer::executeCB, this, _1), false),
        action_name_(name)
    {
        if (!conveyor_.isConnected())
        {
            ROS_ERROR("Conveyor not connected");
        }
        as_.start();
        ROS_INFO("Conveyor Action Server started");
    }

    void executeCB(const hw_t::ConveyorGoalConstPtr &goal)
    {
        int cmd = goal->cmd;

        int slave = 4;     // ✅ fixed as requested
        // int32_t speed = 0; // ✅ NOT fixed, driver decides / default

        if (!conveyor_.isConnected())
        {
            result_.success = false;
            result_.message = "Conveyor not connected";
            as_.setAborted(result_);
            return;
        }

        // 🔥 ALWAYS STOP FIRST (same logic)
        conveyor_.conveyorStop(slave);
        ros::Duration(0.2).sleep();

        switch (cmd)
        {
            case 0:
                feedback_.status = "Conveyor STOPPED";
                break;

            case 1:
                conveyor_.conveyorForward(slave);
                feedback_.status = "FORWARD";
                break;

            case 2:
                conveyor_.conveyorBackward(slave);
                feedback_.status = "BACKWARD";
                break;

            case 3:
                conveyor_.resetAlarm(slave);
                break;

            default:
                result_.success = false;
                result_.message = "Invalid command";
                as_.setAborted(result_);
                return;
        }

        as_.publishFeedback(feedback_);

        result_.success = true;
        result_.message = "Command executed";
        as_.setSucceeded(result_);
    }
};

int main(int argc, char **argv)
{
    ros::init(argc, argv, "conveyor_action_server");
    ConveyorActionServer server("conveyor_action");
    ros::spin();
    return 0;
}