#!/usr/bin/env python3
import rospy
import actionlib
from std_msgs.msg import String
from actionlib_msgs.msg import GoalStatus
from hw_t.msg import (
    machineControlAction,
    machineControlResult,
    machineControlFeedback
)
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler, euler_from_quaternion
from pymongo import MongoClient


class MachineControlServer:

    def __init__(self):
        rospy.init_node("machine_control_server")

        # Mongo connection
        mongo = MongoClient("mongodb://localhost:27017/")
        db = mongo["amcl_data"]
        self.collection = db["Pose_data"]

        # move_base client
        self.movebase = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        rospy.loginfo("Waiting for move_base...")
        self.movebase.wait_for_server()
        rospy.loginfo("Connected to move_base")

        # action server
        self.server = actionlib.SimpleActionServer(
            "machine_control",
            machineControlAction,
            execute_cb=self.execute_cb,
            auto_start=False
        )
        self.server.start()

        # states
        self.pause = False
        self.abort = False
        self.aborted_forever = False
        self.mb_goal = None

        rospy.Subscriber("/goal_control", String, self.control_cb)

        rospy.loginfo("Machine Control Server Ready")

    # --------------------------------------------------

    def publish_feedback(self, control_status):
        feedback = machineControlFeedback()
        state = self.movebase.get_state()
        feedback.move_base_state = GoalStatus.to_string(state)
        feedback.control_status = control_status
        self.server.publish_feedback(feedback)

    # --------------------------------------------------

    def fetch_pose(self, name):
        doc = self.collection.find_one({"name": name})

        if not doc:
            rospy.logerr("❌ Pose name not found in Mongo: %s", name)
            return None

        try:
            amcl = doc["amclData"]["pose"]["pose"]
            pos = amcl["position"]
            ori = amcl["orientation"]

            q = [ori["x"], ori["y"], ori["z"], ori["w"]]
            roll, pitch, yaw = euler_from_quaternion(q)

            return pos["x"], pos["y"], yaw

        except Exception as e:
            rospy.logerr("Mongo parse error: %s", e)
            return None

    # --------------------------------------------------

    def control_cb(self, msg):

        cmd = msg.data.upper()

        if cmd == "ABORT":
            rospy.logerr("🛑 HARD ABORT — system locked")

            self.abort = True
            self.pause = False
            self.aborted_forever = True

            self.movebase.cancel_all_goals()
            self.mb_goal = None

            self.publish_feedback("HARD_ABORT")
            return

        if self.aborted_forever:
            rospy.logerr("SYSTEM LOCKED — waiting for new client goal")
            return

        mb_state = self.movebase.get_state()

        if cmd == "PAUSE":
            rospy.logwarn("⏸ PAUSE")
            self.pause = True
            if mb_state in [GoalStatus.ACTIVE, GoalStatus.PENDING]:
                self.movebase.cancel_goal()
            self.publish_feedback("PAUSED")

        elif cmd == "RESUME":
            rospy.loginfo("▶ RESUME")
            self.pause = False
            if self.mb_goal and mb_state not in [
                GoalStatus.ACTIVE,
                GoalStatus.PENDING
            ]:
                self.movebase.send_goal(self.mb_goal)
            self.publish_feedback("RESUMED")

    # --------------------------------------------------

    def execute_cb(self, goal):

        if self.aborted_forever:
            rospy.logwarn("New goal → clearing abort lock")
            self.aborted_forever = False
            self.abort = False
            self.pause = False

        result = machineControlResult()

        pose = self.fetch_pose(goal.name)
        if pose is None:
            result.success = False
            self.server.set_aborted(result)
            return

        x, y, yaw = pose

        rospy.loginfo("Fetched pose → x=%.3f y=%.3f yaw=%.3f", x, y, yaw)

        self.mb_goal = MoveBaseGoal()
        self.mb_goal.target_pose.header.frame_id = "map"
        self.mb_goal.target_pose.header.stamp = rospy.Time.now()
        self.mb_goal.target_pose.pose.position.x = x
        self.mb_goal.target_pose.pose.position.y = y

        q = quaternion_from_euler(0, 0, yaw)
        self.mb_goal.target_pose.pose.orientation.x = q[0]
        self.mb_goal.target_pose.pose.orientation.y = q[1]
        self.mb_goal.target_pose.pose.orientation.z = q[2]
        self.mb_goal.target_pose.pose.orientation.w = q[3]

        self.movebase.send_goal(self.mb_goal)

        rate = rospy.Rate(10)

        while not rospy.is_shutdown():

            if self.abort:
                rospy.logerr("Execution aborted → full stop")

                result.success = False
                self.server.set_aborted(result)
                self.publish_feedback("HARD_ABORT")

                self.abort = False
                self.pause = False
                self.mb_goal = None
                return

            if self.pause:
                rate.sleep()
                continue

            state = self.movebase.get_state()

            if state == GoalStatus.ACTIVE:
                self.publish_feedback("RUNNING")

            elif state == GoalStatus.SUCCEEDED:
                rospy.loginfo("Goal finished. Waiting for next client.")

                result.success = True
                self.server.set_succeeded(result)
                self.publish_feedback("COMPLETED")

                self.mb_goal = None
                self.pause = False
                self.abort = False
                return

            elif state in [GoalStatus.ABORTED, GoalStatus.REJECTED]:
                rospy.logerr("Move base failed")

                result.success = False
                self.server.set_aborted(result)
                self.publish_feedback("FAILED")

                self.mb_goal = None
                self.pause = False
                self.abort = False
                return

            if self.server.is_preempt_requested():
                rospy.logwarn("Client preempted goal")

                self.movebase.cancel_goal()
                self.server.set_preempted()
                self.mb_goal = None
                return

            rate.sleep()


if __name__ == "__main__":
    MachineControlServer()
    rospy.spin()
