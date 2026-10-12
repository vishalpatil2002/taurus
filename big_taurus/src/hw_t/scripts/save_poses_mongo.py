#!/usr/bin/env python3

import rospy
from nav_msgs.msg import Odometry
from pymongo import MongoClient
import tf

class PoseSaver:
    def __init__(self):
        rospy.init_node("pose_saver")

        # MongoDB
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["simulation_db"]
        self.collection = self.db["robot_positions"]

        rospy.Subscriber("/odom", Odometry, self.odom_cb)

        rospy.loginfo("Pose Saver Node Started")
        rospy.loginfo("Press CTRL+C to stop")

        self.latest_pose = None

        # Initialize incremental _id from last document
        last_doc = self.collection.find_one(sort=[("_id", -1)])
        self.next_id = last_doc["_id"] + 1 if last_doc else 1

    def odom_cb(self, msg):
        self.latest_pose = msg.pose.pose

    def save_position(self, task_name):
        if not self.latest_pose:
            rospy.logwarn("No pose received yet")
            return

        orientation = self.latest_pose.orientation
        (_, _, yaw) = tf.transformations.euler_from_quaternion(
            [orientation.x, orientation.y, orientation.z, orientation.w]
        )

        # Use _id as simple incremental integer
        doc = {
            "_id": self.next_id,
            "task": task_name,
            "x": self.latest_pose.position.x,
            "y": self.latest_pose.position.y,
            "z": self.latest_pose.position.z,
            "yaw": yaw,
            "timestamp": rospy.Time.now().to_sec()
        }

        self.collection.insert_one(doc)
        rospy.loginfo("Saved pose #%d for task: %s", self.next_id, task_name)

        self.next_id += 1

if __name__ == "__main__":
    saver = PoseSaver()

    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        cmd = input("Press ENTER to save pose (or type task name): ")
        task = cmd if cmd else "unknown_task"
        saver.save_position(task)
        rate.sleep()
