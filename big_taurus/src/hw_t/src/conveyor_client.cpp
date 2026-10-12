#include <ros/ros.h>
#include <actionlib/client/simple_action_client.h>
#include "hw_t/ConveyorAction.h"
#include <iostream>

int main(int argc, char **argv)
{
    ros::init(argc, argv, "conveyor_action_client");

    actionlib::SimpleActionClient<hw_t::ConveyorAction> ac("conveyor_action", true);
    ROS_INFO("Waiting for server...");
    ac.waitForServer();

    char cmd;

    std::cout << "\n===== CONVEYOR CONTROL =====\n";
    std::cout << "0 - STOP\n";
    std::cout << "1 - FORWARD\n";
    std::cout << "2 - BACKWARD\n";
    std::cout << "3 - RESET ALARM\n";
    std::cout << "q - QUIT\n\n";

    while (ros::ok())
    {
        std::cout << "Enter command: ";
        std::cin >> cmd;

        if (cmd == 'q') break;

        hw_t::ConveyorGoal goal;

        if      (cmd == '0') goal.cmd = 0;
        else if (cmd == '1') goal.cmd = 1;
        else if (cmd == '2') goal.cmd = 2;
        else if (cmd == '3') goal.cmd = 3;
        else
        {
            std::cout << "Invalid command\n";
            continue;
        }

        ac.sendGoal(goal);
        ac.waitForResult();

        auto result = ac.getResult();
        std::cout << "Result: " << result->message << std::endl;
    }

    return 0;
}