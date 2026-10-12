#!/usr/bin/env python3

import rospy
import actionlib
from pylogix import PLC
from hw_t.msg import machineControlAction, machineControlGoal


PLC_IP = "192.168.3.8"
PLC_TAG = "STN41.PLC_LOAD_REQ"


def plc_request():

    with PLC() as plc:
        plc.IPAddress = PLC_IP
        tag = plc.Read(PLC_TAG)

        if tag.Status == "Success":
            return tag.Value
        else:
            rospy.logerr("PLC Read Error: %s", tag.Status)
            return False


if __name__ == "__main__":

    rospy.init_node("pose_name_client")

    # Check PLC first
    req = plc_request()

    if not req:
        rospy.logwarn("PLC request FALSE → not sending goal")
        exit()

    rospy.loginfo("PLC request TRUE → sending goal")

    client = actionlib.SimpleActionClient(
        "machine_control",
        machineControlAction
    )

    rospy.loginfo("Waiting for server...")
    client.wait_for_server()

    goal = machineControlGoal()
    goal.name = "new"

    rospy.loginfo("Sending pose goal...")
    client.send_goal(goal)

    rospy.loginfo("Goal sent")