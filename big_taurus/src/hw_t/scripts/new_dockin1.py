#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import redis
import actionlib
# from hw_t.msg import  machineControlAction,  machineControlFeedback, machineControlResult
from hw_t.msg import (
    machineControlAction,
    machineControlResult,
    machineControlFeedback
)
import time
import tf
from tf.transformations import euler_from_quaternion
red=redis.Redis(host='localhost',port=6379)
import rospy
from math import pi, sqrt, fabs, atan2, sin, cos
from geometry_msgs.msg import Twist
from nav_msgs.msg import Path
class ScanActionServer:
    def __init__(self,camera_topic,cmd_vel_topic):
        # self.server = actionlib.SimpleActionServer('scan_control',  machineControlAction, self.execute_callback, False)
        # self.server.start()
        # self.cmd_vel_pub = rospy.Publisher('/robot/cmd_vel', Twist, queue_size=1)
        # self.red = redis.Redis(host='localhost', port='6379')
        self.return_back = False
        self.detecting = False
        self.goal = None
        red.set("a","go")
        self.ro=0
        self.cmd_vel_pub = rospy.Publisher(cmd_vel_topic, Twist, queue_size=1)
        rospy.Subscriber(camera_topic, LaserScan, self.scan_callback)
        self.a_server = actionlib.SimpleActionServer(
            "Table_dock",  machineControlAction, execute_cb=self.execute_cb, auto_start=False)
        self.a_server.start()
        print("server_initialize")
        self.listener = tf.TransformListener()

    # def align_to_yaw(self, target_yaw):
    #     rate = rospy.Rate(50)

    #     # normalize input to (-pi, pi)
    #     target_yaw = (target_yaw + pi) % (2*pi) - pi

    #     while not rospy.is_shutdown():
    #         # get current yaw
    #         try:
    #             (trans, rot) = self.listener.lookupTransform("odom", "base_link", rospy.Time(0))
    #             roll, pitch, yaw = euler_from_quaternion(rot)
    #         except:
    #             rate.sleep()
    #             continue

    #         # compute yaw error
    #         yaw_error = target_yaw - yaw
    #         yaw_error = (yaw_error + pi) % (2*pi) - pi  # normalize

    #         # stop condition (< 2 degrees)
    #         if fabs(yaw_error) < 0.035:
    #             break

    #         # simple P-controller (no need full PID for docking rotation)
    #         angular_speed = 0.8 * yaw_error     # kp = 0.8
    #         angular_speed = max(min(angular_speed, 0.3), -0.3)

    #         twist = Twist()
    #         twist.angular.z = angular_speed
    #         self.cmd_vel_pub.publish(twist)

    #         rate.sleep()

    #     # stop robot
    #     self.cmd_vel_pub.publish(Twist())
    #     self.ro = 1


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
          
            if self.error==True:
                self.result.distance_reached = "error"
            else:
                self.result.distance_reached = "Detection completed"
            
            self.a_server.set_aborted(self.result)


        


    def scan_callback(self, scan_data):
        twist = Twist()
        # distance = int(red.get('distance'))
        # distance=400

        
        # distance = red.get('distance')
        # distance=int(distance)
        if not self.detecting:
            red.set('a','go')
            # si=red.get('dock')
            # si=int(si)
            # si=si+1
            # red.set('dock',str(si))
            return 
        # if 175 <= distance <= 310:
        #     self.detecting = False
        if red.get("stop")==b"false":
             self.detecting = False
        s=rospy.get_param("/distance_goal_qr", self.goal)
        print(s)
        if s==0:
            self.detecting = False
            self.error=True
            rospy.set_param("/distance_goal_qr", 1)
            rospy.set_param('/navigation',3)
        try:        
            r1= rospy.get_param("/pauseplay")
            while r1=='paused':
                r1= rospy.get_param("/pauseplay")
                pass
        except:
            rospy.set_param("/pauseplay","dughv")


        for i, range_distance in enumerate(scan_data.ranges):
            angle = scan_data.angle_min + i * scan_data.angle_increment
            # distance = red.get('distance')
            # distance=int(distance)
            # s=rospy.get_param("/distance_goal_qr", self.goal)
            # print(s)
            # if s==0:
            #     self.detecting = False

            # if (distance <900):
            if 2.18<=angle<=2.5 and range_distance>0.8 and (red.get('w')==b'e'):
                    print(range_distance,angle)
                    # distance=red.get('distance')
                    # distance=int(distance)
                    rospy.set_param("/distance_goal_qr", 1)
                    red.set('w','s')

                    rospy.set_param('/navigation',3)
                    # si=red.get('dock')
                    # si=int(si)
                    # si=si+1
                    # time.sleep(5)

                    # red.set('dock',str(si))
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
                
            # if -1.30<=angle<=-0.65 and red.get('a')==b'w':
            
            #         if range_distance==0:
            #             continue
            #         if 0.05<=range_distance<=0.5:
            #             twist.angular.z=-0.0
            #             twist.linear.x=0
            #             self.cmd_vel_pub.publish(twist)
            #             print("rotatinge2")
            #             # print(f"Angle: {angle:.2f} radians, Distance: {range_distance:.2f} meters1")
            #             return
            # if -1.81<=angle<=-1.30 and red.get('a')==b'w':
            
            #         if range_distance==0:
            #             continue
            #         if 0.05<=range_distance<=0.5:
            #             twist.angular.z=-0.0
            #             twist.linear.x=0
            #             self.cmd_vel_pub.publish(twist)
            #             print("rotatinge2")
            #             # print(f"Angle: {angle:.2f} radians, Distance: {range_distance:.2f} meters1")
            #             return
            # if -2.18<=angle<=-1.81 and red.get('a')==b'w':
            
            #         if range_distance==0:
            #             continue
            #         if 0.05<=range_distance<=1:
            #             twist.angular.z=-0.0
            #             twist.linear.x=0
            #             self.cmd_vel_pub.publish(twist)
            #             print("rotatinge2")
            #             # print(f"Angle: {angle:.2f} radians, Distance: {range_distance:.2f} meters1")
            #             return
            if 0.1<=angle<=1.5 and red.get('a')==b'go':
            
                    if range_distance==0:
                        continue
                    if 0.05<=range_distance<=0.8:
                        twist.angular.z=-0.02
                        # twist.linear.x=0
                        self.cmd_vel_pub.publish(twist)
                        print("rotatinge2")
                        # print(f"Angle: {angle:.2f} radians, Distance: {range_distance:.2f} meters1")
                        return
            # if 2.18<=angle<=2.5 and red.get('a')==b'w':
            #     if range_distance>0.6:
            #         print("more distance to dock")
            #         # ok = self.align_to_yaw( -0.7854)
            #         # # wait for self.ro to be set (but with sleep to avoid tight loop)
            #         # wait_start = rospy.get_time()
            #         # while self.ro == 0 and not rospy.is_shutdown():
            #         #     if rospy.get_time() - wait_start > 10.0:
            #         #         rospy.logwarn("waiting for rotate_by_angle took too long")
            #         #         break
            #         #     rospy.sleep(0.05)
            #         rospy.set_param("/distance_goal_qr", 1)
            #         red.set('w','s')

            #         rospy.set_param('/navigation',3)
            #         self.result.distance_reached = "error"
            #         self.error=True
            #         self.detecting = False
            #         return
            if 2.30 <= angle <= 2.40:
                
                self.feedback.reached = "reaching"
                self.a_server.publish_feedback(self.feedback)
                if range_distance == 0.0:
                    continue
                    print("hitting ")
                elif 0.55 <= range_distance <= 0.57:
                    # red.set("a","w")
                    print("set redis")
                    twist.angular.z = 0.00   #need to check accuracy anbd update
                    twist.linear.x = 0.05
                    print(f"Angle: {angle:.2f} radians, Distance: {range_distance:.2f} meters2")
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
           
                 
                    # else:
                    #     twist.angular.z=0
                    #     self.cmd_vel_pub.publish(twist)           
            if 2.30<=angle<=2.40:
            #   print(angle)
              
              if range_distance==0.0:
                  continue
                  
              elif 0.53<=range_distance <0.55:
                  twist.angular.z=-0.02
                #   twist.linear.x=0
                #   red.set("a","w")
                  print(angle)
                  print("rotating 2g")
                
                  # angle = scan_data.angle_min + i * scan_data.angle_increment
                #   print(f"Angle: {angle:.2f} radians, Distance: {distance:.2f} meters chiwehnc")
                  self.cmd_vel_pub.publish(twist)
                  return
              else:
                #   twist.angular.z=0
                  twist.linear.x=0.05
                #   print("A**")
                #   red.set("a","w")
              
                  self.cmd_vel_pub.publish(twist)
            # if -2.08<=angle<=-2.0:
            #     print(angle,range_distance)
            #     if 0.05<=range_distance<=2:
            #         if 0.8<=range_distance<=1:
            #             twist.angular.z=0.02
            #             twist.linear.x=0.0
            #             print("wyhg")
            #             # input()
            #             self.cmd_vel_pub.publish(twist)
            #         elif 1<=range_distance<1.1:
            #             twist.angular.z=-0.02
            #             twist.linear.x=0.0
            #             print("qsxhoiqw")
            #             # input()
            #             self.cmd_vel_pub.publish(twist)

            #         else:
            #             twist.angular.z=0
            #             self.cmd_vel_pub.publish(twist)
            # if 2.15<=angle<=2.18:
            #     # print(angle,range_distance,"wehbd")
                
            #     if 0<=range_distance<=6:
            #         print(range_distance)
            #         if 0.41<=range_distance<=0.52:
            #             print(range_distance)
            #             twist.angular.z=0.0
            #             twist.linear.x=0.02
            #             self.cmd_vel_pub.publish(twist)
            #             print("fkfnwqiuefbq")
            #         elif 0.4<=range_distance<=0.:
            #             print(range_distance)
            #             twist.angular.z=0.0
            #             twist.linear.x=0.02
            #             self.cmd_vel_pub.publish(twist)
            #             print("deokfnhiug3")

            #         elif range_distance<0.35:
            #             twist.angular.z=-0.02
            #             self.cmd_vel_pub.publish(twist)
            #         else:
            #             twist.angular.z=-0.02
            #             self.cmd_vel_pub.publish(twist)

            #     else:
            #             twist.linear.x=0.02
            #             twist.angular.z=0.0'
            #             self.cmd_vel_pub.publish(twist)
if __name__ == '__main__':
    rospy.init_node("aruco_detect", anonymous=True)
    red = redis.Redis(host='localhost', port='6379')

    # calib_data_path = "/home/ssapl/testbot1_ws/src/hw_t/calib_data/MultiMatrix.npz"
    # marker_size = 6.5  # centimeters
    camera_topic = "/scan"
    cmd_vel_topic = "robot/cmd_vel"

    aruco_detector = ScanActionServer( camera_topic, cmd_vel_topic)
    
    rospy.Rate(100)
    rospy.spin()
  