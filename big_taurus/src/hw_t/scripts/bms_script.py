#!/usr/bin/env python3
import serial
import time


uart_config = {
    "port": "/dev/ttyUSB2",  
    "baudrate": 9600,
    "bytesize": serial.EIGHTBITS,
    "parity": serial.PARITY_NONE,
    "stopbits": serial.STOPBITS_ONE,
    "timeout": 2, 
}

def calculate_checksum(data):
    return sum(data) & 0xFF

def send_command(command_id):
    try:
        with serial.Serial(**uart_config) as ser:
            command = [0xA5, 0x40, command_id, 0x08] + [0x00] * 8
            checksum = calculate_checksum(command)
            command.append(checksum)

            # print(f"Sending Command for ID {hex(command_id)}:", [hex(x) for x in command])
            ser.write(bytes(command))  

            time.sleep(1)  
            
            response = ser.read(12)  
            # print(f"Received Response for ID {hex(command_id)}:", response)
            return response
    except serial.SerialException as e:
        print(f"Error communicating with UART: {e}")
        return None
def parse_voltage_current_response(response):
    """Parse response from Command ID 0x90."""
    if len(response) < 8:
        print("Incomplete response for voltage and current.")
        return None

    cumulative_voltage = int.from_bytes(response[4:6], byteorder='big') * 0.1  # V
    acquisition_voltage = int.from_bytes(response[6:8], byteorder='big') * 0.1  # V
    current = (int.from_bytes(response[8:10], byteorder='big') - 30000) * 0.1  # A
    soc = int.from_bytes(response[10:12], byteorder='big') * 0.1  # %
    # soc1=round((float(soc)),2)
    
    

    return {
        "cumulative_voltage": cumulative_voltage,
        "acquisition_voltage": acquisition_voltage,
        "current": current,
        "soc": soc
    }




def parse_mos_status_response(response):
    """Parse response from Command ID 0x93."""

    if len(response) < 12:
        print("Incomplete response for MOS status.")
        return None
    print("actual charge state",response[4])
    
    global charge_state,count
    
    # charge_state = response[4]
    charge_state = charge_state
    charge_mos_status = response[5]
    discharge_mos_status = response[6]
    bms_life = response[7]
    remaining_capacity = int.from_bytes(response[8:12], byteorder='big')
    
    if response[4] == 0:
        count = count+1
        print("**************",count)
        if count == 3:
                charge_state = 0
        else :
            print(count)
            if response[4]==2:
                charge_state = 2
            if response[4]==1:
                charge_state = 1
            else:
                 charge_state = charge_state
        print("@@@@@@@@@@@@@@@@",charge_state)
    if response[4]==2:
                charge_state = 2
                count = 0
    if response[4]==1:
                charge_state = 1
                count = 0

    

    return {
        "charge_state": charge_state,
        "charge_mos_status": charge_mos_status,
        "discharge_mos_status": discharge_mos_status,
        "bms_life": bms_life,
        "remaining_capacity": remaining_capacity
    }

def main():
    
    voltage_current_response = send_command(0x90)
    voltage_current_data = parse_voltage_current_response(voltage_current_response)

    mos_status_response = send_command(0x93)
    mos_status_data = parse_mos_status_response(mos_status_response)

    if voltage_current_data:
        print("\nVoltage and Current Data:")
        print(f"Cumulative Voltage: {voltage_current_data['cumulative_voltage']} V")
        print(f"Acquisition Voltage: {voltage_current_data['acquisition_voltage']} V")
        print(f"Current: {voltage_current_data['current']} A")
        print(f"SOC: {voltage_current_data['soc']} %")

    if mos_status_data:
        print("\nMOS Status Data:")
        print(f"Charge State: {mos_status_data['charge_state']} (0: Rest, 1: Charging, 2: Discharging)")
        print(f"Charge MOS Status: {mos_status_data['charge_mos_status']} (0: Off, 1: On)")
        print(f"Discharge MOS Status: {mos_status_data['discharge_mos_status']} (0: Off, 1: On)")
        print(f"BMS Life: {mos_status_data['bms_life']} cycles")
        print(f"Remaining Capacity: {mos_status_data['remaining_capacity']} mAh")

if __name__ == "__main__":
    global count
    global charge_state
    charge_state = 7
    count = 0
    while True:
        try:
            time.sleep(1)
            main()
        except KeyboardInterrupt:
            print("exception")


# Voltage and Current Data:
# Cumulative Voltage: 52.400000000000006 V
# Acquisition Voltage: 0.0 V
# Current: 15.200000000000001 A
# SOC: 20.5 %

# MOS Status Data:
# Charge State: 1 (0: Rest, 1: Charging, 2: Discharging)
# Charge MOS Status: 1 (0: Off, 1: On)
# Discharge MOS Status: 1 (0: Off, 1: On)
# BMS Life: 154 cycles
# Remaining Capacity: 20500 mAh