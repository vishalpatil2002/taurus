# #!/usr/bin/env python3
# import rospy
# import actionlib
# from std_msgs.msg import String
# from hw_t.msg import machineControlAction
# # from hw_t.msg import  machineControlGoal
# # , aruco_detectGoal
# from hw_t.msg import (
#     machineControlAction,
#     machineControlGoal
   
# )

# class PoseTaskClient:
#     def __init__(self):
#         rospy.init_node("pose_task_client")

#         self.client = actionlib.SimpleActionClient("machine_control", machineControlAction)
#         rospy.loginfo("Waiting for action server...")
#         self.client.wait_for_server()
#         rospy.loginfo("Connected to action server")

#         self.dock_client = actionlib.SimpleActionClient("Table_dock", machineControlAction)
#         rospy.loginfo("Waiting for docking server...")
#         self.dock_client.wait_for_server()
#         rospy.loginfo("Connected to docking server")

#         rospy.Subscriber("/machine_control/feedback", String, self.feedback_cb)

#         self.aborted_forever = False

#     # --------------------------------------------------

#     def feedback_cb(self, msg):
#         rospy.loginfo("Server feedback: %s", msg.data)

#         if msg.data == "SUCCEEDED":
#             rospy.loginfo("Navigation done → start docking")
#             self.start_docking()

#     # --------------------------------------------------

#     def start_docking(self):
#         rospy.loginfo("Starting docking...")

#         goal = aruco_detectGoal()
#         goal.detect = 1

#         rospy.set_param("/distance_goal_qr", 1)

#         self.dock_client.send_goal(goal)
#         self.dock_client.wait_for_result()

#         result = self.dock_client.get_result()

#         if result.distance_reached!="Detection completed":
#             self.start_docking()
#             # print("the result is", result.distance_reached)
#             rospy.loginfo("Dock result: %s", result.distance_reached)
#         else:
#             rospy.logwarn("Dock returned no result")


# # --------------------------------------------------

# if __name__ == "__main__":
#     PoseTaskClient()
#     rospy.spin()


#!/usr/bin/env python3

import rospy
import actionlib
from hw_t.msg import machineControlAction, machineControlGoal


if __name__ == "__main__":
    rospy.init_node("pose_name_client")

    client = actionlib.SimpleActionClient(
        "machine_control",   # change if needed
        machineControlAction
    )

    rospy.loginfo("Waiting for server...")
    client.wait_for_server()
    rospy.loginfo("Connected to server")

    goal = machineControlGoal()
    goal.name = "march_13"   # <-- your pose name

    rospy.loginfo("Sending pose name...")
    client.send_goal(goal)

    rospy.loginfo("Goal sent. Exiting without waiting.")