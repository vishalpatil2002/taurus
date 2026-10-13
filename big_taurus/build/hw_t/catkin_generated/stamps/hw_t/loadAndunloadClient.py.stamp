#!/usr/bin/env python3

import rospy
import actionlib
from pylogix import PLC
from hw_t.msg import machineControlAction, machineControlGoal


PLC_IP = "192.168.3.8"

PLC_LOAD_TAG = "STN41.PLC_LOAD_REQ"
PLC_UNLOAD_TAG = "STN41.PLC_UNLOAD_REQ"


def read_plc():

    with PLC() as plc:

        plc.IPAddress = PLC_IP

        load_tag = plc.Read(PLC_LOAD_TAG)
        unload_tag = plc.Read(PLC_UNLOAD_TAG)

    load_req = False
    unload_req = False

    if load_tag.Status == "Success":
        load_req = load_tag.Value

    if unload_tag.Status == "Success":
        unload_req = unload_tag.Value

    return load_req, unload_req


if __name__ == "__main__":

    rospy.init_node("plc_request_client")

    load_req, unload_req = read_plc()

    if not load_req and not unload_req:
        rospy.logwarn("No PLC request → goal not sent")
        exit()

    client = actionlib.SimpleActionClient(
        "machine_control",
        machineControlAction
    )

    rospy.loginfo("Waiting for machine_control server...")
    client.wait_for_server()

    goal = machineControlGoal()
    

    if load_req:
        goal.operation = "LOAD"
        goal.name = "STN41"

    elif unload_req:
        goal.operation = "UNLOAD"
        goal.name = "STN41"

    rospy.loginfo("Sending goal → %s", goal.operation)

    client.send_goal(goal)

    rospy.loginfo("Goal sent once")