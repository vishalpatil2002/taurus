#!/usr/bin/env python3
import rospy
import actionlib
# from hw_t.msg import machineControlAction, machineControlGoal

from hw_t.msg import (
    machineControlAction,
    machineControlGoal
   
)


def feedback_cb(msg):
        print("feedback:",msg)
def call_server():
    print("gg")
    client2 = actionlib.SimpleActionClient('conveyor_pick', machineControlAction)
    print("wait for server")
    client2.wait_for_server()
    print("server found")
    goal =  machineControlGoal()
    result = 0
    goal =  machineControlGoal()
    goal.detect = 1
    client2.send_goal(goal, feedback_cb=feedback_cb)
    client2.wait_for_result()
    result = client2.get_result()
    print("the result is", result.distance_reached)
def call_dock():

    client3 = actionlib.SimpleActionClient('Table_dock', machineControlAction)
    client3.wait_for_server()
    goal =  machineControlGoal()
    result = 0
    goal =  machineControlGoal()
    goal.detect = 1
    rospy.set_param("/distance_goal_qr",goal.detect )

    client3.send_goal(goal, feedback_cb=feedback_cb)
    client3.wait_for_result()
    result = client3.get_result()
    if result.distance_reached!="Detection completed":
        print(result.distance_reached)
        input("sjnijni")

        call_dock()
    print("the result is", result.distance_reached)

if __name__ == '__main__':

    try:
        rospy.init_node('action_client')
        # result = call_server()
        
        # print ('The result is:', result)
        result2=call_dock()
        print ('The result is:', result2)
    except rospy.ROSInterruptException as e:
        print ('Something went wrong:', e)