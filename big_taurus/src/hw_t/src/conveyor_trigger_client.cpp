#include <ros/ros.h>
#include <actionlib/client/simple_action_client.h>
#include "hw_t/ConveyorAction.h"
#include <iostream>

void feedbackCB(const hw_t::ConveyorFeedbackConstPtr& fb)
{
    std::cout << "Feedback - Current State: "
              << fb->current_state << std::endl;
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "conveyor_client");

    actionlib::SimpleActionClient<hw_t::ConveyorAction>
        ac("conveyor_action", true);

    ROS_INFO("Waiting for conveyor_action server...");
    ac.waitForServer();
    ROS_INFO("Connected.");

    std::cout << "0=STOP  1=FORWARD  2=BACKWARD  q=quit\n";

    while (ros::ok())
    {
        std::string input;
        std::cout << "> ";
        std::cin >> input;

        if (input == "q")
            break;

        int mode;

        try {
            mode = std::stoi(input);
        }
        catch (...)
        {
            std::cout << "Invalid input\n";
            continue;
        }

        hw_t::ConveyorGoal goal;
        goal.mode = mode;

        ac.sendGoal(goal,
                    actionlib::SimpleActionClient<hw_t::ConveyorAction>::SimpleDoneCallback(),
                    actionlib::SimpleActionClient<hw_t::ConveyorAction>::SimpleActiveCallback(),
                    &feedbackCB);

        bool finished = ac.waitForResult(ros::Duration(10.0));

        if (!finished)
        {
            ROS_WARN("Timeout. Cancelling goal.");
            ac.cancelGoal();
            continue;
        }

        auto state = ac.getState();

        if (state == actionlib::SimpleClientGoalState::SUCCEEDED)
            std::cout << "Result: "
                      << ac.getResult()->message << std::endl;
        else
            std::cout << "Action failed: "
                      << state.toString() << std::endl;
    }

    return 0;
}

