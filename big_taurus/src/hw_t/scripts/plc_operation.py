#!/usr/bin/env python3
from pylogix import PLC

with PLC() as plc:

    plc.IPAddress = "192.168.3.8"
  

    # READ
    tag = plc.Read("STN41.PLC_LOAD_REQ")
    print("Read Status:", tag.Status)
    print("Read Value:", tag.Value)

    # WRITE
    # write_result = plc.Write("STN41.AMR_LOAD_ACCEPTED", False)
    # print("Write Status:", write_result.Status)
    # print("write Value:", write_result.Value)

# #!/usr/bin/env python3

# from pylogix import PLC

# PLC_IP = "192.168.3.8"

# TEST_TAG = "STN41.PLC_LOAD_REQ"

# with PLC() as plc:
#     plc.IPAddress = PLC_IP

#     print("=" * 40)
#     print(f"Connecting to PLC  ip={PLC_IP}")
#     print("=" * 40)

#     ret = plc.Read(TEST_TAG)

#     print(f"Tag    : {TEST_TAG}")
#     print(f"Value  : {ret.Value}")
#     print(f"Status : {ret.Status}")

#     if ret.Status == "Success":
#         print("PLC is WORKING")
#     else:
#         print("PLC connection FAILED")

#     print("=" * 40)


