#!/usr/bin/env python3

import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseWithCovarianceStamped
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque

MAX_LEN = 2000

ekf_x = deque(maxlen=MAX_LEN)
ekf_y = deque(maxlen=MAX_LEN)

amcl_x = deque(maxlen=MAX_LEN)
amcl_y = deque(maxlen=MAX_LEN)


def ekf_cb(msg):
    ekf_x.append(msg.pose.pose.position.x)
    ekf_y.append(msg.pose.pose.position.y)


def amcl_cb(msg):
    amcl_x.append(msg.pose.pose.position.x)
    amcl_y.append(msg.pose.pose.position.y)


rospy.init_node("trajectory_compare", anonymous=True)

rospy.Subscriber(
    "/odometry/filtered",
    Odometry,
    ekf_cb,
    queue_size=10
)

rospy.Subscriber(
    "/amcl_pose",
    PoseWithCovarianceStamped,
    amcl_cb,
    queue_size=10
)

fig, ax = plt.subplots()


def update(frame):
    ax.clear()

    if len(ekf_x) > 1:
        ax.plot(ekf_x, ekf_y, label="EKF Odometry", linewidth=2, color="blue")
        ax.scatter(ekf_x[-1], ekf_y[-1], marker='x', color="blue")

    if len(amcl_x) > 1:
        ax.plot(amcl_x, amcl_y, label="AMCL Pose", linewidth=2, color="red")
        ax.scatter(amcl_x[-1], amcl_y[-1], marker='o', color="red")

    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_title("EKF vs AMCL Trajectory Comparison")
    ax.grid(True)
    ax.legend(loc="best")


ani = FuncAnimation(fig, update, interval=100)

plt.show()
