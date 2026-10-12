#!/usr/bin/env python3

import rospy
import tf2_ros
import tf2_geometry_msgs
import math

from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped
from tf.transformations import euler_from_quaternion


# Global variables
odom1 = None
odom2 = None
tf_buffer = None

# Thresholds
X_THRESHOLD = 0.05      # meters
Y_THRESHOLD = 0.05      # meters
YAW_THRESHOLD = 0.05    # radians


def quaternion_to_yaw(q):
    quaternion = [q.x, q.y, q.z, q.w]
    _, _, yaw = euler_from_quaternion(quaternion)
    return yaw


def normalize_angle(angle):
    while angle > math.pi:
        angle -= 2.0 * math.pi

    while angle < -math.pi:
        angle += 2.0 * math.pi

    return angle


def transform_odom_to_map(odom_msg):
    global tf_buffer

    try:
        pose = PoseStamped()
        pose.header = odom_msg.header
        pose.pose = odom_msg.pose.pose

        transformed_pose = tf_buffer.transform(
            pose,
            "odom",
            rospy.Duration(0.5)
        )

        return transformed_pose

    except Exception as e:
        rospy.logwarn("TF Transform Failed: %s", str(e))
        return None


def odom_callback_1(msg):
    global odom1
    odom1 = msg
    compare_poses()


def odom_callback_2(msg):
    global odom2
    odom2 = msg
    compare_poses()


def compare_poses():
    global odom1, odom2

    if odom1 is None or odom2 is None:
        return

    pose1 = transform_odom_to_map(odom1)
    pose2 = transform_odom_to_map(odom2)

    if pose1 is None or pose2 is None:
        return

    x1 = pose1.pose.position.x
    y1 = pose1.pose.position.y
    yaw1 = quaternion_to_yaw(
        pose1.pose.orientation
    )

    x2 = pose2.pose.position.x
    y2 = pose2.pose.position.y
    yaw2 = quaternion_to_yaw(
        pose2.pose.orientation
    )

    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    dyaw = abs(
        normalize_angle(yaw1 - yaw2)
    )

    rospy.loginfo(
        "X Diff: %.4f m | Y Diff: %.4f m | Yaw Diff: %.2f deg",
        dx,
        dy,
        math.degrees(dyaw)
    )

    if dx > X_THRESHOLD:
        rospy.logwarn(
            "X mismatch detected -> %.4f meters",
            dx
        )

    if dy > Y_THRESHOLD:
        rospy.logwarn(
            "Y mismatch detected -> %.4f meters",
            dy
        )

    if dyaw > YAW_THRESHOLD:
        rospy.logwarn(
            "Yaw mismatch detected -> %.2f degrees",
            math.degrees(dyaw)
        )


if __name__ == "__main__":

    rospy.init_node("compare_odom_node")

    tf_buffer = tf2_ros.Buffer()
    tf_listener = tf2_ros.TransformListener(
        tf_buffer
    )

    rospy.Subscriber(
        "/odometry/filtered",
        Odometry,
        odom_callback_1,
        queue_size=1
    )

    rospy.Subscriber(
        "/taurus/mobile_base_controller/odom",
        Odometry,
        odom_callback_2,
        queue_size=1
    )

    rospy.loginfo(
        "Comparing odometry topics in map frame..."
    )

    rospy.spin()