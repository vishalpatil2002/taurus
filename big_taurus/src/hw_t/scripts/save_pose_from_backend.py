#!/usr/bin/env python3
import rospy
import uuid
from pymongo import MongoClient
from geometry_msgs.msg import PoseWithCovarianceStamped


class MongoPoseSaver:
    def __init__(self, pose_name):
        rospy.init_node("mongo_pose_saver")

        self.pose_name = pose_name

        mongo = MongoClient("mongodb://localhost:27017/")
        db = mongo["amcl_data"]
        self.collection = db["Pose_data"]

        rospy.Subscriber("/amcl_pose",
                         PoseWithCovarianceStamped,
                         self.cb)

        self.saved = False
        rospy.loginfo("Mongo Pose Saver Ready")

    def cb(self, msg):

        if self.saved:
            return

        doc = {
            "_id": str(uuid.uuid4()),
            "name": self.pose_name,   # 🔥 user input name
            "mapName": ["dummy_map_name"],      # better as array
            "amclData": {
                "header": {
                    "seq": msg.header.seq,
                    "stamp": {
                        "secs": msg.header.stamp.secs,
                        "nsecs": msg.header.stamp.nsecs
                    },
                    "frame_id": msg.header.frame_id
                },
                "pose": {
                    "pose": {
                        "position": {
                            "x": msg.pose.pose.position.x,
                            "y": msg.pose.pose.position.y,
                            "z": msg.pose.pose.position.z
                        },
                        "orientation": {
                            "x": msg.pose.pose.orientation.x,
                            "y": msg.pose.pose.orientation.y,
                            "z": msg.pose.pose.orientation.z,
                            "w": msg.pose.pose.orientation.w
                        }
                    },
                    "covariance": list(msg.pose.covariance)
                }
            },
            "Description": None
        }

        self.collection.update_one(
            {"name": self.pose_name},
            {"$set": doc},
            upsert=True
        )

        rospy.loginfo("✅ Pose saved to MongoDB")
        rospy.loginfo("ID: %s", doc["_id"])

        self.saved = True


if __name__ == "__main__":

    pose_name = input("Enter pose name to save: ")

    MongoPoseSaver(pose_name)
    rospy.spin()