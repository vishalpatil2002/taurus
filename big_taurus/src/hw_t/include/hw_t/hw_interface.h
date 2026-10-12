#pragma once

#include <hardware_interface/joint_state_interface.h>
#include <hardware_interface/joint_command_interface.h>
#include <hardware_interface/robot_hw.h>
#include <joint_limits_interface/joint_limits.h>
#include <joint_limits_interface/joint_limits_interface.h>
#include <joint_limits_interface/joint_limits_rosparam.h>
#include <controller_manager/controller_manager.h>
#include <boost/shared_ptr.hpp>
#include <ros/ros.h>
#include "hw_t/moonsModbus.h"

class Taurus : public hardware_interface::RobotHW 
{
public:
    Taurus(ros::NodeHandle& nh);
    ~Taurus();

    void init();
    void update(const ros::TimerEvent& e);
    void read();
    void write(ros::Duration elapsed_time);

protected:
    // --- ROS
    ros::NodeHandle nh_;
    ros::Timer non_realtime_loop_;
    double loop_hz_;
    ros::Duration elapsed_time_;
    boost::shared_ptr<controller_manager::ControllerManager> controller_manager_;

    bool shutting_down_;

    // --- Joints
    std::vector<std::string> joint_name_;
    std::vector<double> joint_position_;
    std::vector<double> joint_velocity_;
    std::vector<double> joint_effort_;
    std::vector<double> joint_velocity_command_;

    // --- Interfaces
    hardware_interface::JointStateInterface joint_state_interface_;
    hardware_interface::VelocityJointInterface velocity_joint_interface_;
    joint_limits_interface::VelocityJointSaturationInterface velocityJointSaturationInterface;

    // --- Motors
    boost::shared_ptr<Moons> moons_;
    int left_inv_;
    int right_inv_;
    int gear_ratio_;
    double counts_per_rev_;
    double left_prev_cmd_;
    double right_prev_cmd_;
};
