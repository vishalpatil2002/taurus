#include <ros/ros.h>
#include <actionlib/server/simple_action_server.h>
#include "hw_t/LiftAction.h"
#include "lift_control.h"

class LiftActionServer
{
private:
    ros::NodeHandle nh_;
    actionlib::SimpleActionServer<hw_t::LiftAction> as_;
    std::string action_name_;

    hw_t::LiftFeedback feedback_;
    hw_t::LiftResult result_;

    Moons lift_;

public:
    LiftActionServer(std::string name) :
        as_(nh_, name, boost::bind(&LiftActionServer::executeCB, this, _1), false),
        action_name_(name)
    {
        if (!lift_.isConnected())
        {
            ROS_ERROR("Lift not connected");
        }
        as_.start();
        ROS_INFO("Lift Action Server started");
    }

    void executeCB(const hw_t::LiftGoalConstPtr &goal)
    {
        int cmd   = goal->cmd;
        int slave = goal->slave;

        feedback_.status = "Command received";
        as_.publishFeedback(feedback_);

        if (!lift_.isConnected())
        {
            result_.success = false;
            result_.message = "Lift not connected";
            as_.setAborted(result_);
            return;
        }

        switch (cmd)
        {
            case 1:
                lift_.liftUp(slave);
                feedback_.status = "Lift moving UP";
                break;

            case 2:
                lift_.liftDown(slave);
                feedback_.status = "Lift moving DOWN";
                break;

            case 3:
                lift_.stopLift(slave);
                feedback_.status = "Lift STOPPED";
                break;

            case 4:
                lift_.resetAlarm(slave);
                feedback_.status = "Alarm RESET";
                break;

            default:
                result_.success = false;
                result_.message = "Invalid command";
                as_.setAborted(result_);
                return;
        }

        as_.publishFeedback(feedback_);
        ros::Duration(0.5).sleep();   // simulate action duration

        result_.success = true;
        result_.message = "Command executed successfully";
        as_.setSucceeded(result_);
    }
};

int main(int argc, char **argv)
{
    ros::init(argc, argv, "lift_action_server");
    LiftActionServer server("lift_action");
    ros::spin();
    return 0;
}
