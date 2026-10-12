#!/usr/bin/env python
from pymodbus.client import ModbusTcpClient

PLC_IP = "192.168.7.5"   # change to your PLC IP
PLC_ID = 1               # Modbus slave ID

client = ModbusTcpClient(PLC_IP, port=502)
client.connect()


# Write M10 = 1 (True)- to overwrite, false-on
result = client.write_coil(address=10, value=True, slave=PLC_ID) # for safety feature off
#result = client.write_coil(address=10, value=False, slave=PLC_ID)

if not result.isError():
    print("M10 set to 1")
else:
    print("Modbus write error")

client.close()
