#!/usr/bin/env python3
# =============================================================================
#  test_stn41.py
#  Bridge: PLC <---> ROS Machine Control
#  Handles: PLC polling → Handshake → Conveyor Trigger → PLC ACK
# =============================================================================

import rospy
import actionlib
from pylogix import PLC
from std_msgs.msg import String
from hw_t.msg import (
    machineControlAction,
    machineControlGoal,
    machineControlResult,
    machineControlFeedback,
)

# =============================================================================
# CONFIGURATION
# =============================================================================
PLC_IP    = "192.168.3.8"   # Allen-Bradley PLC IP
PREFIX    = "STN41"         # Tag folder in PLC (e.g., STN41.PLC_LOAD_REQ)
POSE_NAME = "new"           # The name of the pose in MongoDB
# =============================================================================

SEP  = "=" * 60
SEP2 = "-" * 60

def log(msg): rospy.loginfo(f"[{PREFIX}] {msg}")
def logerr(msg): rospy.logerr(f"[{PREFIX}] {msg}")

# ── PLC Helpers ───────────────────────────────────────────────────────────────

def plc_read(plc, tag):
    """Reads a boolean tag from the PLC."""
    full_tag = f"{PREFIX}.{tag}"
    ret = plc.Read(full_tag)
    if ret.Status == "Success":
        return bool(ret.Value)
    return False

def plc_write(plc, tag, value=True):
    """Writes a value to a PLC tag."""
    full_tag = f"{PREFIX}.{tag}"
    ret = plc.Write(full_tag, value)
    if ret.Status == "Success":
        log(f"PLC WRITE SUCCESS: {full_tag} = {value}")
    else:
        logerr(f"PLC WRITE FAILED: {full_tag} Status: {ret.Status}")

def wait_for_tag(plc, tag, target=True, timeout=60):
    """Blocks until a PLC tag reaches the target value."""
    log(f"Waiting for {PREFIX}.{tag} to be {target}...")
    start_time = rospy.get_time()
    rate = rospy.Rate(5)
    while not rospy.is_shutdown():
        if plc_read(plc, tag) == target:
            log(f"PLC confirmed {tag} is {target}")
            return True
        if (rospy.get_time() - start_time) > timeout:
            logerr(f"Timeout waiting for {tag}")
            return False
        rate.sleep()
    return False

# ── Sequence Logic ───────────────────────────────────────────────────────────

def execute_sequence(task_type, plc, conv_pub):
    """
    Unified function for LOAD and UNLOAD sequences.
    task_type: "LOAD" or "UNLOAD"
    """
    log(SEP)
    log(f"STARTING {task_type} SEQUENCE")
    log(SEP)

    # 1. Accept the Request in PLC
    plc_write(plc, f"AMR_{task_type}_ACCEPTED", True)

    # 2. Connect to ROS Machine Control Server
    client = actionlib.SimpleActionClient("machine_control", machineControlAction)
    if not client.wait_for_server(rospy.Duration(5.0)):
        logerr("Machine Control Server not found!")
        return

    goal = machineControlGoal()
    goal.name = POSE_NAME
    goal.task_name = task_type

    def feedback_cb(fb):
        status = fb.control_status.strip().upper()
        
        # --- DOCKING PHASE ---
        if status == "DOCKING DONE":
            log(f"Robot Docked. Starting {task_type} Handshake...")
            
            if task_type == "LOAD":
                # LOAD HANDSHAKE
                plc_write(plc, "AMR_DOCK_COMPLETE_LOAD", True)
                plc_write(plc, "AMR_START_TRANSFER", True)
                log("Waiting for PLC_TRANSFER_ACCEPTED...")
                if wait_for_tag(plc, "PLC_TRANSFER_ACCEPTED"):
                    log("Handshake Complete. Starting AMR Conveyor FORWARD.")
                    conv_pub.publish("FORWARD")
            
            else:
                # UNLOAD HANDSHAKE
                plc_write(plc, "AMR_DOCK_COMPLETE_UNLOAD", True)
                log("Waiting for PLC_START_TRANSFER...")
                if wait_for_tag(plc, "PLC_START_TRANSFER"):
                    plc_write(plc, "AMR_TRANSFER_ACCEPTED", True)
                    log("Handshake Complete. Starting AMR Conveyor REVERSE.")
                    conv_pub.publish("REVERSE")

        # --- CONVEYOR PHASE ---
        elif status == "CONVEYOR DONE":
            log(f"AMR Conveyor finished. Finalizing PLC {task_type} ACKs...")
            
            if task_type == "LOAD":
                plc_write(plc, "AMR_TRANSFER_COMPLETE", True)
                if wait_for_tag(plc, "PLC_PALLET_RECEIVED"):
                    plc_write(plc, "AMR_TRANSFER_ACK_LOAD", True)
            
            else:
                if wait_for_tag(plc, "PLC_TRANSFER_COMPLETE"):
                    plc_write(plc, "AMR_TRANSFER_ACK_UNLOAD", True)
            
            log(f"SEQUENCE {task_type} FULLY COMPLETED")

        elif status == "RUNNING":
            log("Robot is currently navigating...")

    # Send goal and wait
    client.send_goal(goal, feedback_cb=feedback_cb)
    client.wait_for_result()
    
    # Cleanup PLC tags for next run
    log("Resetting Request-Accept Tags...")
    plc_write(plc, f"AMR_{task_type}_ACCEPTED", False)

# ── Main Loop ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    rospy.init_node("test_stn41")
    
    # Publisher to trigger the actual conveyor movement in the Unified Server
    conv_pub = rospy.Publisher("/conveyor/cmd", String, queue_size=1)
    
    log(SEP)
    log(f"STN41 PLC BRIDGE ACTIVE - IP: {PLC_IP}")
    log(SEP)

    with PLC() as plc:
        plc.IPAddress = PLC_IP
        
        rate = rospy.Rate(5) # Poll PLC at 5Hz
        while not rospy.is_shutdown():
            
            # Check for UNLOAD Request
            if plc_read(plc, "PLC_UNLOAD_REQ"):
                log("PLC_UNLOAD_REQ detected!")
                execute_sequence("UNLOAD", plc, conv_pub)
            
            # Check for LOAD Request
            elif plc_read(plc, "PLC_LOAD_REQ"):
                log("PLC_LOAD_REQ detected!")
                execute_sequence("LOAD", plc, conv_pub)

            rate.sleep()