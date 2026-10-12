#!/usr/bin/env python3
"""
Simple Network Check with PLC Trigger
Uses PING only - no TCP ports
"""

import rospy
import subprocess
import time
from threading import Thread
from pymodbus.client import ModbusTcpClient

class NetworkCheck:
    def __init__(self):
        rospy.init_node('network_check', anonymous=False)
        
        # Configuration
        self.target_host = '192.168.3.243'
        self.plc_ip = '192.168.7.5'
        self.plc_bit = 32
        self.check_interval = 5
        self.retry_count = 3
        
        # Modbus client
        self.modbus = ModbusTcpClient(host=self.plc_ip, port=502)
        self.modbus.connect()
        
        self.connected = False
        self.is_running = False
        
        rospy.loginfo(f"Network Check initialized - Target: {self.target_host}")
        rospy.loginfo(f"PLC: {self.plc_ip}:502 - Bit: M{self.plc_bit}")
    
    def ping_host(self):
        """Test connectivity using PING"""
        try:
            result = subprocess.run(
                ['ping', '-c', '1', '-W', '2', self.target_host],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    def set_plc_bit(self, value):
        """Set PLC bit via Modbus"""
        try:
            if not self.modbus.is_socket_open():
                self.modbus.connect()
            
            self.modbus.write_coil(address=self.plc_bit, value=value, slave=1)
            status = "TRUE" if value else "FALSE"
            rospy.loginfo(f"✓ PLC M{self.plc_bit} = {status}")
            return True
        except Exception as e:
            rospy.logerr(f"✗ PLC write error: {e}")
            return False
    
    def retry_ping(self):
        """Retry ping with exponential backoff"""
        for i in range(self.retry_count):
            rospy.loginfo(f"  Retry {i+1}/{self.retry_count}...")
            if self.ping_host():
                rospy.loginfo("  ✓ Connection restored!")
                return True
            if i < self.retry_count - 1:
                wait_time = 2 ** i
                rospy.loginfo(f"  ⏳ Waiting {wait_time}s...")
                time.sleep(wait_time)
        return False
    
    def monitor(self):
        """Main monitoring loop"""
        rospy.loginfo("Starting network monitoring...")
        
        # Initial check
        is_connected = self.ping_host()
        self.connected = is_connected
        self.set_plc_bit(is_connected)
        rospy.loginfo(f"Initial status: {'CONNECTED' if is_connected else 'DISCONNECTED'}")
        
        # Continuous check
        while self.is_running and not rospy.is_shutdown():
            time.sleep(self.check_interval)
            
            is_connected = self.ping_host()
            
            # Status changed
            if is_connected != self.connected:
                self.connected = is_connected
                
                if is_connected:
                    rospy.loginfo("✓ Network CONNECTED!")
                    self.set_plc_bit(True)
                else:
                    rospy.logerr("✗ Network DISCONNECTED! Retrying...")
                    if self.retry_ping():
                        rospy.loginfo("✓ Reconnected!")
                        self.set_plc_bit(True)
                    else:
                        rospy.logerr("✗ Reconnection failed! Triggering alarm...")
                        time.sleep(2)  # Wait before trigger
                        self.set_plc_bit(False)
    
    def start(self):
        """Start monitoring thread"""
        self.is_running = True
        Thread(target=self.monitor, daemon=False).start()
    
    def stop(self):
        """Stop monitoring"""
        self.is_running = False
        if self.modbus:
            self.modbus.close()


if __name__ == '__main__':
    try:
        nc = NetworkCheck()
        nc.start()
        rospy.spin()
        nc.stop()
    except rospy.ROSInterruptException:
        pass