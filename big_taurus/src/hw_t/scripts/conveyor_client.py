#!/usr/bin/env python3

import rospy
import actionlib
from hw_t.msg import ConveyorAction, ConveyorGoal


def conveyor_feedback_cb(feedback):
    rospy.loginfo("Feedback - Current State: %s", feedback.current_state)


def send_goal(client, mode):
    goal = ConveyorGoal()
    goal.mode = mode

    rospy.loginfo("Sending mode: %d", mode)

    client.send_goal(goal, feedback_cb=conveyor_feedback_cb)

    finished = client.wait_for_result(rospy.Duration(10))

    if not finished:
        rospy.logwarn("Timeout. Cancelling goal.")
        client.cancel_goal()
    else:
        result = client.get_result()
        rospy.loginfo("Result: %s", result.message)


def main():

    rospy.init_node("conveyor_client")

    client = actionlib.SimpleActionClient("conveyor_action", ConveyorAction)

    rospy.loginfo("Waiting for conveyor_action server...")
    client.wait_for_server()
    rospy.loginfo("Connected")

    rospy.sleep(2)

    # FORWARD
    if red.get("conveyor_transfer")==b'True':
        send_goal(client, 1)
        red.set("conveyor_transfer","False")
    if red.get("conveyor_receive")==b'True':
        send_goal(client, 2)
        red.set("conveyor_receive","False")
        
    while(red.get("sensor"))!= True:
        pass
    send_goal(client, 0)
    red.set("sensor","False")


  

    # STOP
    # send_goal(client, 0)
    # rospy.sleep(3)

    # # BACKWARD
    # send_goal(client, 2)

    # rospy.sleep(10)

    # # STOP
    # send_goal(client, 0)

    return "conveyor operation finished"


if __name__ == "__main__":
    result = main()
    print(result)