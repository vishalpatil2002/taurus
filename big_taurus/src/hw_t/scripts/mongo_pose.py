#!/usr/bin/env python3

import rospy
import actionlib
from pymongo import MongoClient
from hw_t.msg import machineControlAction, machineControlResult


class MachineServer:

    def __init__(self):
        rospy.init_node("machine_control_server")

        mongo = MongoClient("mongodb://localhost:27017/")
        db = mongo["amcl_data"]
        self.collection = db["Pose_data"]

        self.server = actionlib.SimpleActionServer(
            "machine_control",
            machineControlAction,
            execute_cb=self.execute_cb,
            auto_start=False
        )

        self.server.start()
        rospy.loginfo("✅ Test server ready — logging only")

    # --------------------------------------------------

    def execute_cb(self, goal):

        pose_name = goal.name.strip()
        rospy.loginfo("📩 Requested pose name: %s", pose_name)

        doc = self.collection.find_one({"name": pose_name})

        if not doc:
            rospy.logerr("❌ Pose NOT found in Mongo")
            self.server.set_aborted()
            return

        amcl = doc["amclData"]["pose"]["pose"]
        pos = amcl["position"]
        ori = amcl["orientation"]

        rospy.loginfo("✅ Pose found")
        rospy.loginfo("Position → x=%.3f y=%.3f z=%.3f",
                      pos["x"], pos["y"], pos.get("z", 0))
        rospy.loginfo("Orientation → x=%.3f y=%.3f z=%.3f w=%.3f",
                      ori["x"], ori["y"], ori["z"], ori["w"])

        # 🔴 NO robot movement — logging only

        result = machineControlResult()
        result.success = True
        self.server.set_succeeded(result)

        rospy.loginfo("✅ Test result returned")


# --------------------------------------------------

if __name__ == "__main__":
    MachineServer()
    rospy.spin()
