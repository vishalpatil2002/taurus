#include <ros/ros.h>
#include <actionlib/client/simple_action_client.h>
#include "hw_t/LiftAction.h"
#include <iostream>

int main(int argc, char **argv)
{
    ros::init(argc, argv, "lift_action_client");

    actionlib::SimpleActionClient<hw_t::LiftAction> ac("lift_action", true);
    ROS_INFO("Waiting for lift action server...");
    ac.waitForServer();
    ROS_INFO("Connected to lift action server");

    int slave = 3;
    char cmd;

    std::cout << "1-UP  2-DOWN  3-STOP  4-RESET  q-QUIT\n";

    while (ros::ok())
    {
        std::cin >> cmd;
        if (cmd == 'q') break;

        hw_t::LiftGoal goal;
        goal.slave = slave;

        if      (cmd == '1') goal.cmd = 1;
        else if (cmd == '2') goal.cmd = 2;
        else if (cmd == '3') goal.cmd = 3;
        else if (cmd == '4') goal.cmd = 4;
        else continue;

        ac.sendGoal(goal);
        ac.waitForResult();

        auto result = ac.getResult();
        std::cout << result->message << std::endl;
    }

    return 0;
}
