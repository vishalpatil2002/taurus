#!/usr/bin/env python3

import rospy
from hw_t.msg import bms
import bms_script
# import bms

def main():
    rospy.init_node("bmsnode")
    pub = rospy.Publisher("/bms", bms, queue_size=10)
    rate = rospy.Rate(1)
    rospy.loginfo("BMS Node Started")
    while not rospy.is_shutdown():
        msg = bms()

        try:
            vc_response = bms_script.send_command(0x90)
            vc_data = bms_script.parse_voltage_current_response(vc_response)

            mos_response = bms_script.send_command(0x93)
            mos_data = bms_script.parse_voltage_current_response(mos_response)

            # if vc_data and mos_data:
            #     voltage_cum = vc_data["cumulative_voltage"]
            #     voltage_cum1 = round(voltage_cum,2)
            #     msg.cumulative_voltage = voltage_cum1
            #     soc1 = vc_data["soc"]
            #     soc3 = 12.2324334
            #     soc2= int(soc3)
            #     print(soc2)
            #     msg.soc = soc2
            #     msg.health = "OK"

            if vc_data and mos_data:
                voltage = vc_data["cumulative_voltage"]
                soc = vc_data["soc"]

                msg.cumulative_voltage = int(round(voltage ))
                msg.soc = int(round(soc))
                msg.health = "OK"

                print(msg.cumulative_voltage)





                # rospy.loginfo("Voltage: %.2f%%", msg.cumulative_voltage)
                # rospy.loginfo("SOC: %.2f%%", soc) 67.890


            else:
                raise Exception("Incomplete BMS data")
        except Exception as e:
            rospy.logwarn("BMS read failed,Publishing zeros: %s", str(e))

            msg.cumulative_voltage = 0.0
            msg.soc = 0.0
            msg.health = "Not OK"
    
        pub.publish(msg)
        rate.sleep()

if __name__=="__main__":
    main()