#!/usr/bin/env python3

import rospy
from nav_msgs.msg import Odometry
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque

MAX_LEN = 2000

wheel_x = deque(maxlen=MAX_LEN)
wheel_y = deque(maxlen=MAX_LEN)



def wheel_cb(msg):
    wheel_x.append(msg.pose.pose.position.x)
    wheel_y.append(msg.pose.pose.position.y)



rospy.init_node("odom_compare", anonymous=True)

rospy.Subscriber(
    "taurus/mobile_base_controller/odom",
    Odometry,
    wheel_cb,
    queue_size=10
)



fig, ax = plt.subplots()

def update(frame):
    ax.clear()

    if len(wheel_x) > 1:
        ax.plot(wheel_x, wheel_y, '--', label="Wheel Odometry")

   
    if wheel_x:
        ax.scatter(wheel_x[-1], wheel_y[-1], marker='o')

  

    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_title("Wheel Odometry")
    ax.grid(True)
    ax.legend()

ani = FuncAnimation(fig, update, interval=100)

plt.show()
