#!/usr/bin/env python3
import threading
import rospy
import actionlib
import math

from std_msgs.msg        import String
from actionlib_msgs.msg  import GoalStatus
from geometry_msgs.msg   import Twist
from sensor_msgs.msg     import LaserScan
from nav_msgs.msg        import Odometry
from move_base_msgs.msg  import MoveBaseAction, MoveBaseGoal
from tf.transformations  import quaternion_from_euler, euler_from_quaternion
from pymongo             import MongoClient

from hw_t.msg import (
    machineControlAction,
    machineControlGoal,
    machineControlResult,
    machineControlFeedback,
    ConveyorAction,
    ConveyorGoal,
)

class UnifiedMachineServer:
    def __init__(self):
        rospy.init_node("machine_control_server")

        # --- MongoDB Connection ---
        mongo = MongoClient("mongodb://localhost:27017/")
        self.collection = mongo["amcl_data"]["Pose_data"]
        
        # --- State ---
        self.abort = False
        self.current_yaw = 0.0
        self._conveyor_cmd = None
        self._conveyor_event = threading.Event()

        # --- ROS Clients ---
        self.cmd_pub = rospy.Publisher("/robot/cmd_vel", Twist, queue_size=10)
        self.movebase = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        self.conv_cli = actionlib.SimpleActionClient("conveyor_action", ConveyorAction)

        # --- Subscribers ---
        rospy.Subscriber('/odometry/filtered', Odometry, self._odom_cb)
        rospy.Subscriber("/conveyor/cmd", String, self._conveyor_cmd_cb)
        rospy.Subscriber("/goal_control", String, self._control_cb)

        # --- Action Server ---
        self.server = actionlib.SimpleActionServer(
            "machine_control", machineControlAction, self._execute_cb, False
        )
        self.server.start()
        rospy.loginfo("✅ Unified Machine Server is fully operational.")

    def _odom_cb(self, msg):
        q = msg.pose.pose.orientation
        _, _, self.current_yaw = euler_from_quaternion([q.x, q.y, q.z, q.w])

    def _conveyor_cmd_cb(self, msg):
        cmd = msg.data.strip().upper()
        if cmd in ("FORWARD", "REVERSE"):
            self._conveyor_cmd = cmd
            self._conveyor_event.set()

    def _control_cb(self, msg):
        if msg.data.strip().upper() == "ABORT":
            self.abort = True
            self.movebase.cancel_all_goals()
            self.conv_cli.send_goal(ConveyorGoal(mode=0))

    def _rotate_90(self):
        rospy.loginfo("[DOCK] Rotating 90 degrees...")
        target_yaw = math.atan2(math.sin(self.current_yaw + math.pi/2), 
                                math.cos(self.current_yaw + math.pi/2))
        rate = rospy.Rate(20)
        while not rospy.is_shutdown() and not self.abort:
            error = math.atan2(math.sin(target_yaw - self.current_yaw), 
                               math.cos(target_yaw - self.current_yaw))
            if abs(error) < 0.03: break
            t = Twist()
            t.angular.z = max(min(1.0 * error, 0.25), -0.25)
            self.cmd_pub.publish(t)
            rate.sleep()
        self.cmd_pub.publish(Twist())

    def _approach_table(self):
        rospy.loginfo("[DOCK] Approaching table...")
        while not rospy.is_shutdown() and not self.abort:
            try:
                scan = rospy.wait_for_message("/scan", LaserScan, timeout=1.0)
                if scan.ranges[len(scan.ranges)//2] < 0.16: break
                t = Twist()
                t.linear.x = 0.05
                self.cmd_pub.publish(t)
            except: continue
        self.cmd_pub.publish(Twist())

    def _execute_cb(self, goal):
        self.abort = False
        self._conveyor_event.clear()
        res = machineControlResult()
        
        # 1. Fetch from MongoDB
        doc = self.collection.find_one({"name": goal.name})
        if not doc:
            rospy.logerr(f"Pose {goal.name} not found!")
            self.server.set_aborted(res)
            return

        # FIXED: Explicitly map dictionary values to ROS message attributes
        m_pos = doc["amclData"]["pose"]["pose"]["position"]
        m_ori = doc["amclData"]["pose"]["pose"]["orientation"]

        # 2. Build Navigation Goal
        mb_goal = MoveBaseGoal()
        mb_goal.target_pose.header.frame_id = "map"
        mb_goal.target_pose.header.stamp = rospy.Time.now()
        
        mb_goal.target_pose.pose.position.x = m_pos["x"]
        mb_goal.target_pose.pose.position.y = m_pos["y"]
        mb_goal.target_pose.pose.position.z = m_pos.get("z", 0.0)
        
        mb_goal.target_pose.pose.orientation.x = m_ori["x"]
        mb_goal.target_pose.pose.orientation.y = m_ori["y"]
        mb_goal.target_pose.pose.orientation.z = m_ori["z"]
        mb_goal.target_pose.pose.orientation.w = m_ori["w"]

        rospy.loginfo(f"[TASK] Starting {goal.task_name} sequence.")
        self.movebase.send_goal(mb_goal)
        
        while self.movebase.get_state() not in [GoalStatus.SUCCEEDED, GoalStatus.ABORTED]:
            if self.abort: self.server.set_aborted(res); return
            self.server.publish_feedback(machineControlFeedback(control_status="RUNNING"))
            rospy.sleep(0.1)

        # 3. Local Docking
        self.server.publish_feedback(machineControlFeedback(control_status="NAVIGATION COMPLETED"))
        self._rotate_90()
        self._approach_table()
        
        # 4. PLC Handshake Signal
        self.server.publish_feedback(machineControlFeedback(control_status="DOCKING DONE"))
        
        if not self._conveyor_event.wait(timeout=60.0):
            self.server.set_aborted(res); return

        # 5. Conveyor Movement (Triggering your C++ PLC Server)
        mode = 1 if self._conveyor_cmd == "FORWARD" else 2
        self.conv_cli.send_goal(ConveyorGoal(mode=mode))
        
        # Wait for pallet sensor
        rospy.wait_for_message("/conveyor/sensor", String)
        self.conv_cli.send_goal(ConveyorGoal(mode=0)) # STOP
        
        self.server.publish_feedback(machineControlFeedback(control_status="CONVEYOR DONE"))
        rospy.sleep(2.0)

        # 6. Move Back
        t0 = rospy.Time.now().to_sec()
        while (rospy.Time.now().to_sec() - t0) < 16.0:
            t = Twist(); t.linear.x = -0.05
            self.cmd_pub.publish(t)
            rospy.sleep(0.05)
        self.cmd_pub.publish(Twist())
        
        res.success = True
        self.server.set_succeeded(res)

if __name__ == "__main__":
    UnifiedMachineServer()
    rospy.spin()