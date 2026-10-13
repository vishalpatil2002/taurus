#!/usr/bin/env python3

import time
import redis
import rospy
import actionlib
import tf
import math

from math import pi
from tf.transformations import euler_from_quaternion

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

from hw_t.msg import (
    machineControlAction,
    machineControlResult,
    machineControlFeedback,
    machineControlGoal
)

# Redis connection
red = redis.Redis(host='localhost', port=6379)


class ScanActionServer:

    def __init__(self, camera_topic, cmd_vel_topic):

        self.return_back = False
        self.detecting = False
        self.goal = None
        red.set("a","go")
        self.ro=0
        self.docking_completed = False
        self.cmd_vel_pub = rospy.Publisher(cmd_vel_topic, Twist, queue_size=1)
        rospy.Subscriber(camera_topic, LaserScan, self.scan_callback)
        self.a_server = actionlib.SimpleActionServer(
            "Table_dock",  machineControlAction, execute_cb=self.execute_cb, auto_start=False)
        self.a_server.start()
        print("server_initialize")
        self.listener = tf.TransformListener()


        self.cmd_pub = rospy.Publisher('robot/cmd_vel', Twist, queue_size=10)
        rospy.Subscriber('/odometry/filtered', Odometry, self.odom_callback)

        self.current_yaw = None
        self.start_yaw = None
        self.rate = rospy.Rate(20)


    # ================= ODOM CALLBACK =================
    def odom_callback(self, msg):
        orientation_q = msg.pose.pose.orientation
        _, _, yaw = euler_from_quaternion([
            orientation_q.x,
            orientation_q.y,
            orientation_q.z,
            orientation_q.w
        ])
        self.current_yaw = yaw


    def normalize_angle(self, angle):
        """Normalize angle to [-pi, pi]"""
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        return angle




    def rotate(self):
        # Wait for odom
        rospy.loginfo("Waiting for odometry...")
        while self.current_yaw is None and not rospy.is_shutdown():
            self.rate.sleep()

        self.start_yaw = self.current_yaw
        target_yaw = self.normalize_angle(self.start_yaw + math.pi / 2)+math.radians(2)

        rospy.loginfo(f"Start yaw  : {math.degrees(self.start_yaw):.2f} deg")
        rospy.loginfo(f"Target yaw : {math.degrees(target_yaw):.2f} deg")

        twist = Twist()

        tolerance = math.radians(0.1)   # ~0.2 degree accuracy
        max_speed = 0.2
        min_speed = 0.01

        while not rospy.is_shutdown():
            error = self.normalize_angle(target_yaw - self.current_yaw)

            if abs(error) < tolerance:
                break

            # Proportional controller
            angular_speed = 1.5 * error

            # Clamp speed
            angular_speed = max(min(angular_speed, max_speed), -max_speed)

            # Avoid stall near target
            if abs(angular_speed) < min_speed:
                angular_speed = min_speed if angular_speed > 0 else -min_speed

            twist.linear.x = 0.0
            twist.angular.z = angular_speed
            self.cmd_pub.publish(twist)

            self.rate.sleep()

        # Stop robot
        twist.angular.z = 0.0
        self.cmd_pub.publish(twist)

        rospy.loginfo("✔ Robot rotated exactly 90 degrees")


    # def rotate(self, timeout=5.0):

    #     rospy.loginfo("Starting rotation...")

    #     start_time = rospy.Time.now().to_sec()

    #     while self.current_yaw is None and not rospy.is_shutdown():
    #         if rospy.Time.now().to_sec() - start_time > 2.0:
    #             rospy.logwarn("Odometry not available")
    #             return False
    #         self.rate.sleep()

    #     start_yaw = self.current_yaw
    #     target_yaw = self.normalize_angle(start_yaw + math.pi / 2)

    #     twist = Twist()
    #     tolerance = math.radians(0.5)

    #     start_time = rospy.Time.now().to_sec()

    #     while not rospy.is_shutdown():

    #         # 🔴 Preemption check
    #         if self.a_server.is_preempt_requested():
    #             self.a_server.set_preempted()
    #             return False

    #         # 🔴 Timeout check
    #         if rospy.Time.now().to_sec() - start_time > timeout:
    #             rospy.logwarn("Rotation timeout")
    #             break

    #         error = self.normalize_angle(target_yaw - self.current_yaw)

    #         if abs(error) < tolerance:
    #             break

    #         twist.linear.x = 0.0
    #         twist.angular.z = max(min(1.5 * error, 0.2), -0.2)
    #         self.cmd_vel_pub.publish(twist)

    #         self.rate.sleep()

    #     twist.angular.z = 0.0
    #     self.cmd_vel_pub.publish(twist)

    #     rospy.loginfo("Rotation finished")
    #     return True



    def move_forward_until_close(self, target_distance=0.12, speed=0.05):

        rate = rospy.Rate(20)
        twist = Twist()

        while not rospy.is_shutdown():

            scan_msg = rospy.wait_for_message("/scan", LaserScan)

            front_distance = None

            for i, dist in enumerate(scan_msg.ranges):
                angle = scan_msg.angle_min + i * scan_msg.angle_increment

                if 1.00 <= angle <= 1.1:
                    front_distance = dist
                    break

            if front_distance is None:
                rate.sleep()
                continue

            if front_distance <= target_distance:
                twist.linear.x = 0.0
                self.cmd_vel_pub.publish(twist)
                break
            else:
                twist.linear.x = speed
                self.cmd_vel_pub.publish(twist)

            rate.sleep()


    # def move_forward_until_close(self, target_distance=0.12, speed=0.05, timeout=5.0):

    #     rospy.loginfo("Starting forward motion...")

    #     rate = rospy.Rate(20)
    #     start_time = rospy.Time.now().to_sec()
    #     twist = Twist()

    #     while not rospy.is_shutdown():

    #         # 🔴 Preemption check
    #         if self.a_server.is_preempt_requested():
    #             self.a_server.set_preempted()
    #             return False

    #         # 🔴 Timeout check
    #         if rospy.Time.now().to_sec() - start_time > timeout:
    #             rospy.logwarn("Forward timeout")
    #             break

    #         scan_msg = rospy.wait_for_message("/scan", LaserScan)

    #         front_distance = None
    #         for i, dist in enumerate(scan_msg.ranges):
    #             angle = scan_msg.angle_min + i * scan_msg.angle_increment
    #             if 1.00 <= angle <= 1.1:
    #                 front_distance = dist
    #                 break

    #         if front_distance is None:
    #             rate.sleep()
    #             continue

    #         if front_distance <= target_distance:
    #             break

    #         twist.linear.x = speed
    #         self.cmd_vel_pub.publish(twist)

    #         rate.sleep()

    #     twist.linear.x = 0.0
    #     self.cmd_vel_pub.publish(twist)

    #     rospy.loginfo("Forward motion finished")
    #     return True
    





    # ================= EXECUTE CALLBACK =================

    def execute_cb(self, goal):
        self.goal = goal  # Set the goal attribute
        print("goal1")
        rospy.set_param('/navigation',4)
        self.feedback =  machineControlFeedback()
        self.result = machineControlResult()
        self.detecting = True  # Start detecting when a goal is received
        # red.set('a','go')
        self.error=False
        print("e3fn2")
        while not rospy.is_shutdown() and self.detecting:
            if self.a_server.is_preempt_requested():
                rospy.loginfo('Preempted ArucoDetection')
                self.a_server.set_preempted()
                self.detecting = False
                rospy.loginfo('goal_cancel')
                return

            # Detection logic is handled in the callback
            rospy.sleep(0.1)

        if self.detecting:

            red.set('a','go')
            
            self.a_server.set_succeeded(self.result)
        
        elif self.a_server.is_active():
          
            if self.error:
                self.result.distance_reached = "error"
                self.a_server.set_aborted(self.result)
            elif self.docking_completed:
                self.detecting = False
                
                rospy.sleep(2.0)
                print("-----------------")
                self.rotate()
                
                rospy.sleep(2.0)
                self.move_forward_until_close()

                self.result.distance_reached = "Detection completed"
                self.a_server.set_succeeded(self.result)



            # elif self.docking_completed:

            #     self.detecting = False

            #     self.feedback.reached = "Docking!!!!!!!!!!!!!!"
            #     self.a_server.publish_feedback(self.feedback)

            #     # -------- ROTATION --------
            #     self.feedback.reached = "Rotating!!!!!!!!!"
            #     self.a_server.publish_feedback(self.feedback)

            #     if not self.rotate():
            #         self.result.distance_reached = "Rotation failed!!!!!!!!!1"
            #         self.a_server.set_aborted(self.result)
            #         return

            #     # -------- FORWARD --------
            #     self.feedback.reached = "Moving forward!!!!!!!!!!!!!"
            #     self.a_server.publish_feedback(self.feedback)

            #     if not self.move_forward_until_close():
            #         self.result.distance_reached = "Forward failed!!!!!!"
            #         self.a_server.set_aborted(self.result)
            #         return

            #     self.result.distance_reached = "Detection completed"
            #     self.a_server.set_succeeded(self.result) 

  

            else:
                self.result.distance_reached = "docking not completed"
                self.a_server.set_aborted(self.result)
    # ================= SCAN CALLBACK =================

    def scan_callback(self, scan_data):

        twist = Twist()

        if not self.detecting:
            red.set('a', 'go')
            return

        if red.get("stop") == b"false":
            self.detecting = False

        s = rospy.get_param("/distance_goal_qr", self.goal)

        if s == 0:
            self.detecting = False
            self.error = True
            rospy.set_param("/distance_goal_qr", 1)
            rospy.set_param('/navigation', 3)

        try:        
            r1= rospy.get_param("/pauseplay")
            while r1=='paused':
                r1= rospy.get_param("/pauseplay")
                pass
        except:
            rospy.set_param("/pauseplay","dughv")


        for i, range_distance in enumerate(scan_data.ranges):

            angle = scan_data.angle_min + i * scan_data.angle_increment

            # ---- CONDITION 1 ----
            if 2.18 <= angle <= 2.5 and range_distance > 0.8 and red.get('w') == b'e':
                rospy.set_param("/distance_goal_qr", 1)
                red.set('w', 's')
                rospy.set_param('/navigation', 3)
                self.docking_completed = True   # ✅ important
                self.detecting = False


            if 2.18<=angle<=2.2 and 0.2<=range_distance<=0.9:
                s+=1
                if s<=90:
                    rospy.set_param("/distance_goal_qr", s)
                m=rospy.get_param("/distance_goal_qr")
                print(m)
                if m>=90:
                    red.set("a","w")
                    red.set('w','e')

            # ---- OBSTACLE ROTATION ----
            if 0.1 <= angle <= 1.5 and red.get('a') == b'go':

                if range_distance == 0:
                    continue

                if 0.05 <= range_distance <= 0.8:
                    twist.angular.z = -0.02
                    self.cmd_vel_pub.publish(twist)
                    return

            # ---- DOCK ALIGNMENT ----
            if 2.30 <= angle <= 2.40:
                self.feedback.reached = "reaching"
                self.a_server.publish_feedback(self.feedback)

                if range_distance == 0.0:
                    continue

                elif 0.55 <= range_distance <= 0.57:
                    twist.angular.z = 0.0
                    twist.linear.x = 0.05
                    self.cmd_vel_pub.publish(twist)
                    return
                
                elif 0.02 < range_distance <= 1.0:
                    if range_distance>0.57:
                    #   red.set("a","w")
                      twist.angular.z = 0.02
                    #   twist.linear.x=0.0
                      print(f"Angle: {angle:.2f} radians, Distance: {range_distance:.2f} check")
                    #   input()
                    #   print("wigfiuw2iu")
                      self.cmd_vel_pub.publish(twist)
                    elif range_distance<0.55:
                       
                        twist.angular.z=-0.02
                        # twist.linear.x=0
                        self.cmd_vel_pub.publish(twist)
                        print("rotatinge sg")
                        print(f"Angle: {angle:.2f} radians, Distance: {range_distance:.2f} meters")
                        # input()
                else:
                    twist.angular.z = 0.00
                    twist.linear.x = 0.05
                    # print("check")
                    self.cmd_vel_pub.publish(twist)

                

            if 2.30 <= angle <= 2.40:

                if range_distance == 0.0:
                    continue

                elif 0.53 <= range_distance < 0.55:
                    twist.angular.z = -0.02
                    self.cmd_vel_pub.publish(twist)
                    return

                else:
                    twist.linear.x = 0.05
                    self.cmd_vel_pub.publish(twist)


# ================= MAIN =================

if __name__ == '__main__':

    rospy.init_node("aruco_detect", anonymous=True)

    camera_topic = "/scan"
    cmd_vel_topic = "robot/cmd_vel"

    server = ScanActionServer(camera_topic, cmd_vel_topic)
    rospy.Rate(100)
    rospy.spin()