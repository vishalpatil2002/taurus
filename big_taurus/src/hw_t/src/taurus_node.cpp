#include "hw_t/hw_interface.h"
#include "hw_t/moonsModbus.h"

#include <angles/angles.h>
#include <ros/ros.h>
#include <controller_manager/controller_manager.h>

#include <signal.h>
#include <cmath>

// ------------------------------------------------
void sigintHandler(int sig)
{
    ros::shutdown();
}
// ------------------------------------------------

Taurus::Taurus(ros::NodeHandle& nh)
    : nh_(nh), shutting_down_(false)
{
    nh_.param<int>("l_inv", left_inv_, 1);
    nh_.param<int>("r_inv", right_inv_,-1);
    nh_.param<int>("gear_ratio", gear_ratio_, 40);
    nh_.param<double>("counts_per_rev", counts_per_rev_, 10000.0);

    loop_hz_ = 10.0;

    left_prev_cmd_  = 0;
    right_prev_cmd_ = 0;

    joint_name_ = {"right_wheel", "left_wheel"};

    joint_position_.resize(2, 0.0);
    joint_velocity_.resize(2, 0.0);
    joint_effort_.resize(2, 0.0);

    // 🚨 VERY IMPORTANT: start with ZERO command
    joint_velocity_command_.resize(2, 0.0);

    init();

    // ---------- Moons connection ----------
    moons_ = boost::make_shared<Moons>();

    if (!moons_ || !moons_->isConnected())
    {
        ROS_FATAL("Moons motor controller not connected!");
        ros::shutdown();
        return;
    }
    
    moons_->resetAlarm();
    moons_->setEncoder({0,0});
    moons_->startJog();

    // 🔒 FORCE STOP ON STARTUP (clears stored speed in drive)
    moons_->setSpeed(3, 0, 0);

    ROS_INFO("Moons Jog mode enabled (motors stopped)");

    controller_manager_.reset(
        new controller_manager::ControllerManager(this, nh_));

    ros::Duration update_period(1.0 / loop_hz_);
    non_realtime_loop_ =
        nh_.createTimer(update_period, &Taurus::update, this);
}

// ------------------------------------------------

Taurus::~Taurus()
{
    ROS_INFO("Shutting down Taurus hardware interface");
    shutting_down_ = true;

    non_realtime_loop_.stop();   // stop timer FIRST

    if (moons_ && moons_->isConnected())
    {
        // 🔒 FORCE STOP BEFORE EXIT
        moons_->setSpeed(3, 0, 0);
        moons_->stopJog();
        moons_->disableMotor();
        moons_->end();
    }

    moons_.reset();
}

// ------------------------------------------------

void Taurus::init()
{
    for (size_t i = 0; i < joint_name_.size(); ++i)
    {
        hardware_interface::JointStateHandle state_handle(
            joint_name_[i],
            &joint_position_[i],
            &joint_velocity_[i],
            &joint_effort_[i]);

        joint_state_interface_.registerHandle(state_handle);

        hardware_interface::JointHandle vel_handle(
            state_handle,
            &joint_velocity_command_[i]);

        velocity_joint_interface_.registerHandle(vel_handle);

        joint_limits_interface::JointLimits limits;
        joint_limits_interface::getJointLimits(joint_name_[i], nh_, limits);

        joint_limits_interface::VelocityJointSaturationHandle limit_handle(
            vel_handle, limits);

        velocityJointSaturationInterface.registerHandle(limit_handle);
    }

    registerInterface(&joint_state_interface_);
    registerInterface(&velocity_joint_interface_);
    registerInterface(&velocityJointSaturationInterface);
}

// ------------------------------------------------

void Taurus::update(const ros::TimerEvent& e)
{
    if (shutting_down_) return;

    ros::Duration elapsed_time(e.current_real - e.last_real);

    read();
    controller_manager_->update(ros::Time::now(), elapsed_time);
    write(elapsed_time);
}

// ------------------------------------------------

void Taurus::read()
{
    if (!moons_ || !moons_->isConnected()) return;

    int32_t enc1 = moons_->longRead(10, 1, true, 0) * left_inv_;
    int32_t enc2 = moons_->longRead(10, 2, true, 0) * right_inv_;

    int32_t vel1 = moons_->readRegister(16, 1, true) * left_inv_;
    int32_t vel2 = moons_->readRegister(16, 2, true) * right_inv_;

    joint_position_[0] =
        angles::from_degrees(enc1 * 360.0 / (counts_per_rev_ * gear_ratio_));

    joint_position_[1] =
        angles::from_degrees(enc2 * 360.0 / (counts_per_rev_ * gear_ratio_));

    joint_velocity_[0] =
        angles::from_degrees(vel1 * 360.0 / (240.0 * gear_ratio_));

    joint_velocity_[1] =
        angles::from_degrees(vel2 * 360.0 / (240.0 * gear_ratio_));
}

// ------------------------------------------------

void Taurus::write(ros::Duration elapsed_time)
{
    if (!moons_ || !moons_->isConnected()) return;

    // ---------------- PLC keep-alive ----------------
    moons_->setM0Alive();
    // ------------------------------------------------
    //  std::cout<< "moons status" <<moons_->getPLCBit(14);

    // Emergency reset from PLC
    if ((moons_->getPLCBit(14) == 1) && (moons_->getPLCBit(16) == 0) )
    {
       
        moons_->startJog();
    }
    //  std::cout<< "moons status" <<moons_->getPLCBit(16);

    if ( (moons_->getPLCBit(16) == 1) )
    {
        moons_->setSpeed(3, 0, 0);
        moons_->stopJog();
        
    }

    velocityJointSaturationInterface.enforceLimits(elapsed_time);

    long cmd1 = std::round(
        (angles::to_degrees(joint_velocity_command_[0]) / 360.0)
        * 240.0 * gear_ratio_) * left_inv_;

    long cmd2 = std::round(
        (angles::to_degrees(joint_velocity_command_[1]) / 360.0)
        * 240.0 * gear_ratio_) * right_inv_;

    // 🔒 If NO controller command → FORCE STOP ONCE
    if (cmd1 == 0 && cmd2 == 0 &&
        (left_prev_cmd_ != 0 || right_prev_cmd_ != 0))
    {
        moons_->setSpeed(3, 0, 0);
        left_prev_cmd_  = 0;
        right_prev_cmd_ = 0;
        return;
    }

    if ((cmd1 != left_prev_cmd_ || cmd2 != right_prev_cmd_) &&(moons_->getPLCBit(16) == 0))
    {
        int motor_add = 0;
        if (cmd1 != left_prev_cmd_)  motor_add |= 1;
        if (cmd2 != right_prev_cmd_) motor_add |= 2;

        moons_->setSpeed(motor_add, cmd1, cmd2);

        left_prev_cmd_  = cmd1;
        right_prev_cmd_ = cmd2;
    }
}

// ------------------------------------------------

int main(int argc, char** argv)
{
    ros::init(argc, argv,
              "mobile_robot_hardware_interface",
              ros::init_options::NoSigintHandler);

    signal(SIGINT, sigintHandler);

    ros::NodeHandle nh;
    ros::MultiThreadedSpinner spinner(2);

    Taurus robot(nh);
    spinner.spin();

    return 0;
}
