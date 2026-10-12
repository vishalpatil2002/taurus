#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PoseStamped

FILE_PATH="/home/taurus/new_taurus_ws/src/hw_t/config/saved_goal.txt"


def goal_callback(msg:PoseStamped):
    with open(FILE_PATH, "a") as f:
        f.write(
            "x="f"{msg.pose.position.x:.3f}"
            "y="f"{msg.pose.position.y:.3f}"
            "z="f"{msg.pose.orientation.z:.5f}"
            "w="f"{msg.pose.orientation.w:.5f}\n"
        )
        rospy.loginfo("Done")



def main():
    rospy.init_node("goal_sub")
    sub = rospy.Subscriber("/move_base_simple/goal", PoseStamped, goal_callback)
    rospy.loginfo("Waiting for data")
    rospy.spin()

if __name__=="__main__":
    main()