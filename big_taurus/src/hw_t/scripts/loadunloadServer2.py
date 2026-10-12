#!/usr/bin/env python3
import rospy
import actionlib
from std_msgs.msg import String
from actionlib_msgs.msg import GoalStatus
from hw_t.msg import (
    machineControlAction,
    machineControlResult,
    machineControlFeedback,
    machineControlGoal
)
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler, euler_from_quaternion
from pymongo import MongoClient
from geometry_msgs.msg import Twist
from hw_t.msg import ConveyorAction, ConveyorGoal
import redis
from pylogix import PLC
from pymodbus.client import ModbusTcpClient


class MachineControlServer:

    def __init__(self):

        rospy.init_node("machine_control_server")

        mongo = MongoClient("mongodb://localhost:27017/")
        db = mongo["amcl_data"]
        self.collection = db["Pose_data"]

        self.movebase = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        rospy.loginfo("Waiting for move_base...")
        self.movebase.wait_for_server()
        rospy.loginfo("Connected to move_base")

        self.red = redis.Redis(host="localhost", port=6379)
        self.station = None

        self.server = actionlib.SimpleActionServer(
            "machine_control",
            machineControlAction,
            execute_cb=self.execute_cb,
            auto_start=False
        )

        self.server.start()

        self.pause = False
        self.abort = False
        self.aborted_forever = False
        self.mb_goal = None

        rospy.Subscriber("/goal_control", String, self.control_cb)

        self.cmd_pub = rospy.Publisher("/robot/cmd_vel", Twist, queue_size=10)

        rospy.loginfo("Machine Control Server Ready")

    # --------------------------------------------------

    def publish_feedback(self, control_status):

        feedback = machineControlFeedback()

        state = self.movebase.get_state()

        feedback.move_base_state = GoalStatus.to_string(state)
        feedback.control_status = control_status

        self.server.publish_feedback(feedback)

    # --------------------------------------------------

    def plc_read(self, tag):

        try:
            with PLC() as plc:

                plc.IPAddress = "192.168.3.8"

                result = plc.Read(tag)

                if result.Status == "Success":
                    return result.Value

        except Exception as e:

            rospy.logerr("PLC Read Error: %s", e)

        return None

    # --------------------------------------------------

    def plc_write(self, tag, value):

        try:

            with PLC() as plc:

                plc.IPAddress = "192.168.3.8"

                plc.Write(tag, value)

        except Exception as e:

            rospy.logerr("PLC Write Error: %s", e)

    # --------------------------------------------------

    def wait_for_m31(self):

        PLC_IP = "192.168.7.5"
        PLC_ID = 1

        client = ModbusTcpClient(PLC_IP, port=502)

        client.connect()

        while True:

            result = client.read_coils(address=31, count=1, slave=PLC_ID)

            if not result.isError():

                if result.bits[0]:

                    client.close()

                    return True

            rospy.sleep(0.2)

    # --------------------------------------------------

    def fetch_pose(self, name):

        doc = self.collection.find_one({"name": name})

        if not doc:

            rospy.logerr("Pose name not found: %s", name)

            return None

        try:

            amcl = doc["amclData"]["pose"]["pose"]

            pos = amcl["position"]
            ori = amcl["orientation"]

            q = [ori["x"], ori["y"], ori["z"], ori["w"]]

            roll, pitch, yaw = euler_from_quaternion(q)

            return pos["x"], pos["y"], yaw
        
        except Exception as e:
            rospy.logerr("Mongo parse error: %s", e)
            return None

    # --------------------------------------------------

    def control_cb(self, msg):

        cmd = msg.data.upper()

        if cmd == "ABORT":

            rospy.logerr("HARD ABORT")

            self.abort = True
            self.pause = False
            self.aborted_forever = True

            self.movebase.cancel_all_goals()

            self.mb_goal = None

            self.publish_feedback("HARD_ABORT")

            return

        if self.aborted_forever:
            rospy.logerr("SYSTEM LOCKED — waiting for new client goal")

            return

        mb_state = self.movebase.get_state()

        if cmd == "PAUSE":

            rospy.logwarn("PAUSE")

            self.pause = True

            if mb_state in [GoalStatus.ACTIVE, GoalStatus.PENDING]:

                self.movebase.cancel_goal()

            self.publish_feedback("PAUSED")

        elif cmd == "RESUME":

            rospy.loginfo("RESUME")

            self.pause = False

            if self.mb_goal and mb_state not in [
                GoalStatus.ACTIVE,
                GoalStatus.PENDING
            ]:

                self.movebase.send_goal(self.mb_goal)

            self.publish_feedback("RESUMED")

    # --------------------------------------------------

    def move_back(self, distance=0.8, speed=0.05):

        twist = Twist()

        rate = rospy.Rate(20)

        duration = distance / speed

        start_time = rospy.Time.now().to_sec()

        while not rospy.is_shutdown():

            if rospy.Time.now().to_sec() - start_time >= duration:
                break

            twist.linear.x = -speed

            self.cmd_pub.publish(twist)

            rate.sleep()

        twist.linear.x = 0.0

        self.cmd_pub.publish(twist)

        return "BACK_ACTION_COMPLETED"

    # --------------------------------------------------
    # LOAD CONVEYOR
    # --------------------------------------------------

    # def conveyor_client_load(self):

    #     client = actionlib.SimpleActionClient("conveyor_action", ConveyorAction)

    #     client.wait_for_server()

    #     goal = ConveyorGoal()

    #     while self.plc_read(f"{self.station}.PLC_TRANSFER_ACCEPTED") != True:
    #         rospy.loginfo("waiting for plc transfer acceptance")
    #         rospy.loginfo(0.5)

            

    #     goal.mode = 1

    #     client.send_goal(goal)

    #     while self.plc_read(f"{self.station}.PLC_PALLET_RECEIVED") != True:
    #         rospy.loginfo("waiting for plc pallet recived")
    #         rospy.loginfo(0.5)

    #     goal.mode = 0

    #     client.send_goal(goal)

    #     client.wait_for_result()

    #     # self.plc_write(f"{self.station}.AMR_TRANSFER_COMPLETE", True)

    #     # self.plc_write(f"{self.station}.AMR_TRANSFER_ACK_LOAD", True)

    #     return "CONVEYOR OPERATION DONE FOR LOAD"

    # # --------------------------------------------------
    # # UNLOAD CONVEYOR
    # # --------------------------------------------------

    # def conveyor_client_unload(self):

    #     client = actionlib.SimpleActionClient("conveyor_action", ConveyorAction)

    #     client.wait_for_server()

    #     goal = ConveyorGoal()

        

    #     while self.plc_read(f"{self.station}.PLC_START_TRANSFER") != True:
    #         rospy.loginfo("waiting for plc start trnasfer")
    #         rospy.loginfo(0.5)

    #     self.plc_write(f"{self.station}.AMR_TRANSFER_ACCEPTED", True)

    #     goal.mode = 2

    #     client.send_goal(goal)

    #     while self.plc_read(f"{self.station}.PLC_TRANSFER_COMPLETE") != True and self.wait_for_m31():
    #         rospy.loginfo("waiting for plc trnasfer complete")
    #         rospy.loginfo(0.5)

            

    #     goal.mode = 0

    #     client.send_goal(goal)

    #     client.wait_for_result()

    #     return "CONVEYOR OPERATION DONE FOR UNLOAD"


    def conveyor_client_load(self):

        client = actionlib.SimpleActionClient("conveyor_action", ConveyorAction)
        client.wait_for_server()

        goal = ConveyorGoal()

        # ✅ TIMEOUT ADDED
        start = rospy.Time.now()
        while self.plc_read(f"{self.station}.PLC_TRANSFER_ACCEPTED") != True:
            if (rospy.Time.now() - start).to_sec() > 60:
                rospy.logerr("PLC_TRANSFER_ACCEPTED TIMEOUT")
                return "FAILED"
            rospy.loginfo("waiting for plc transfer acceptance")
            rospy.sleep(0.5)

        goal.mode = 1
        client.send_goal(goal)

        # ✅ TIMEOUT ADDED
        start = rospy.Time.now()
        while self.plc_read(f"{self.station}.PLC_PALLET_RECEIVED") != True:
            if (rospy.Time.now() - start).to_sec() > 60:
                rospy.logerr("PLC_PALLET_RECEIVED TIMEOUT")
                goal.mode = 0
                client.send_goal(goal)
                return "FAILED"
            rospy.loginfo("waiting for plc pallet received")
            rospy.sleep(0.5)

        goal.mode = 0
        client.send_goal(goal)
        client.wait_for_result()

        return "CONVEYOR OPERATION DONE FOR LOAD"





    def conveyor_client_unload(self):

        client = actionlib.SimpleActionClient("conveyor_action", ConveyorAction)
        client.wait_for_server()

        goal = ConveyorGoal()

     
        start = rospy.Time.now()
        while self.plc_read(f"{self.station}.PLC_START_TRANSFER") != True:
            if (rospy.Time.now() - start).to_sec() > 60:
                rospy.logerr("PLC_START_TRANSFER TIMEOUT")
                return "FAILED"
            rospy.loginfo("waiting for plc start transfer")
            rospy.sleep(0.5)

        self.plc_write(f"{self.station}.AMR_TRANSFER_ACCEPTED", True)

        goal.mode = 2
        client.send_goal(goal)

        # ✅ TIMEOUT ADDED
        start = rospy.Time.now()
        while self.plc_read(f"{self.station}.PLC_TRANSFER_COMPLETE") != True and self.wait_for_m31():
            if (rospy.Time.now() - start).to_sec() > 60:
                rospy.logerr("PLC_TRANSFER_COMPLETE TIMEOUT")
                goal.mode = 0
                client.send_goal(goal)
                return "FAILED"
            rospy.loginfo("waiting for plc transfer complete")
            rospy.sleep(0.5)

        goal.mode = 0
        client.send_goal(goal)
        client.wait_for_result()

        return "CONVEYOR OPERATION DONE FOR UNLOAD"

    # --------------------------------------------------

    def execute_cb(self, goal):

        if self.aborted_forever:
            rospy.logwarn("New goal → clearing abort lock")
            self.aborted_forever = False
            self.abort = False
            self.pause = False
        self.station = goal.name

        operation = goal.operation.upper()

        result = machineControlResult()

        pose = self.fetch_pose(goal.name)

        if pose is None:

            result.success = False

            self.server.set_aborted(result)

            return

        if operation == "LOAD":

            v = self.plc_write(f"{self.station}.AMR_LOAD_ACCEPTED", True)
            # rospy.loginfo("Write Status:", v.Status)

        elif operation == "UNLOAD":

            self.plc_write(f"{self.station}.AMR_UNLOAD_ACCEPTED", True)

        x, y, yaw = pose

        self.mb_goal = MoveBaseGoal()

        self.mb_goal.target_pose.header.frame_id = "map"

        self.mb_goal.target_pose.header.stamp = rospy.Time.now()

        self.mb_goal.target_pose.pose.position.x = x

        self.mb_goal.target_pose.pose.position.y = y

        q = quaternion_from_euler(0, 0, yaw)

        self.mb_goal.target_pose.pose.orientation.x = q[0]
        self.mb_goal.target_pose.pose.orientation.y = q[1]
        self.mb_goal.target_pose.pose.orientation.z = q[2]
        self.mb_goal.target_pose.pose.orientation.w = q[3]

        self.movebase.send_goal(self.mb_goal)

        rate = rospy.Rate(10)

        while not rospy.is_shutdown():
            if self.abort:
                rospy.logerr("Execution aborted → full stop")

                result.success = False
                self.server.set_aborted(result)
                self.publish_feedback("HARD_ABORT")

                self.abort = False
                self.pause = False
                self.mb_goal = None

            if self.pause:

                rate.sleep()

                continue

            state = self.movebase.get_state()

            if state == GoalStatus.ACTIVE:

                self.publish_feedback("RUNNING")

            elif state == GoalStatus.SUCCEEDED:

                dock_cli = actionlib.SimpleActionClient(
                    "Table_dock", machineControlAction
                )

                dock_cli.wait_for_server()

                dock_goal = machineControlGoal()

                dock_goal.detect = 1
                rospy.set_param("/distance_goal_qr", dock_goal.detect)


                dock_cli.send_goal(dock_goal)

                dock_cli.wait_for_result()

                dock_result = dock_cli.get_result()

                if dock_result.distance_reached == "Detection completed":

                    if operation == "LOAD":

                        self.plc_write(f"{self.station}.AMR_DOCK_COMPLETE_LOAD", True)

                        self.plc_write(f"{self.station}.AMR_START_TRANSFER", True)

                        conveyor_res = self.conveyor_client_load()
                        if conveyor_res == "CONVEYOR OPERATION DONE FOR LOAD":
                            self.plc_write(f"{self.station}.AMR_TRANSFER_COMPLETE", True)
                            self.plc_write(f"{self.station}.AMR_TRANSFER_ACK_LOAD", True)
                            move_back_res = self.move_back()
                            if move_back_res == "BACK_ACTION_COMPLETED":
                                rospy.loginfo("Done back action!!!!!")
                                result.success = True
                                self.server.set_succeeded(result)

                        

                    elif operation == "UNLOAD":

                        self.plc_write(f"{self.station}.AMR_DOCK_COMPLETE_UNLOAD", True)
                        conveyor_res = self.conveyor_client_unload()

                        if conveyor_res ==  "CONVEYOR OPERATION DONE FOR UNLOAD":
                            self.plc_write(f"{self.station}.AMR_TRANSFER_ACK_UNLOAD", True)
                            rospy.sleep(2)
                            move_back_res = self.move_back()
                            if move_back_res == "BACK_ACTION_COMPLETED":
                                rospy.loginfo("Done back action!!!!!")
                                result.success = True
                                self.server.set_succeeded(result)

                else:
                    rospy.loginfo("DOCKING FAILED, RETRYING!!!!!")
                    result.success = False
                    self.server.set_aborted(result)


                self.mb_goal = None
                self.pause = False
                self.abort = False
                return

            elif state in [GoalStatus.ABORTED, GoalStatus.REJECTED]:
                rospy.logerr("Move base failed")

                result.success = False
                self.server.set_aborted(result)
                self.publish_feedback("FAILED")

                self.mb_goal = None
                self.pause = False
                self.abort = False
                return

            if self.server.is_preempt_requested():
                rospy.logwarn("Client preempted goal")

                self.movebase.cancel_goal()
                self.server.set_preempted()
                self.mb_goal = None
                return

            rate.sleep()


                




            

           


if __name__ == "__main__":

    MachineControlServer()

    rospy.spin()