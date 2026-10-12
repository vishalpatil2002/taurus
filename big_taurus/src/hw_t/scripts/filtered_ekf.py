#!/usr/bin/env python3

import rospy
from nav_msgs.msg import Odometry
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque

MAX_LEN = 2000


ekf_x = deque(maxlen=MAX_LEN)
ekf_y = deque(maxlen=MAX_LEN)


def ekf_cb(msg):
    ekf_x.append(msg.pose.pose.position.x)
    ekf_y.append(msg.pose.pose.position.y)

rospy.init_node("EKF_trajectory_compare", anonymous=True)

rospy.Subscriber(
    "/odometry/filtered",
    Odometry,
    ekf_cb,
    queue_size=10
)

fig, ax = plt.subplots()

def update(frame):
    ax.clear()

    if len(ekf_x) > 1:
        ax.plot(ekf_x, ekf_y, label="EKF Odometry", linewidth=2)


    if ekf_x:
        ax.scatter(ekf_x[-1], ekf_y[-1], marker='x')

    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_title(" EKF Odometry Trajectory")
    ax.grid(True)
    ax.legend()

ani = FuncAnimation(fig, update, interval=100)

plt.show()
