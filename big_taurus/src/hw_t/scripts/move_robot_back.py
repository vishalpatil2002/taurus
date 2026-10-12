#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist


class MoveBackNode:

    def __init__(self):

        rospy.init_node("move_back_node")

        # Publisher for robot velocity
        self.cmd_pub = rospy.Publisher("/robot/cmd_vel", Twist, queue_size=10)

        rospy.loginfo("MoveBack node started")

    def move_back(self, distance=0.2, speed=0.05):

        rospy.loginfo("Moving backward")

        twist = Twist()
        rate = rospy.Rate(20)

        # time required to travel the distance
        duration = distance / speed
        start_time = rospy.Time.now().to_sec()

        while not rospy.is_shutdown():

            if rospy.Time.now().to_sec() - start_time >= duration:
                break

            twist.linear.x = -speed
            self.cmd_pub.publish(twist)

            rate.sleep()

        # stop robot
        twist.linear.x = 0.0
        self.cmd_pub.publish(twist)

        rospy.loginfo("Backward motion completed")

        return "BACK_ACTION_COMPLETED"


if __name__ == "__main__":

    robot = MoveBackNode()

    rospy.sleep(1)

    # Move robot back 20 cm
    robot.move_back(distance=0.2, speed=0.05)

    rospy.spin()