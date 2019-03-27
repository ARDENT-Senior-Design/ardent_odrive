#!/usr/bin/env python3
"""
ODrive Position Control Mode
"""
from __future__ import print_function

import odrive
from odrive.enums import *
import time
import math

# Find a connected ODrive (this will block until you connect one)
##########print("finding an odrive...")
##########my_drive = odrive.find_any()
##########print("found odrive")
# Find an ODrive that is connected on the serial port /dev/ttyUSB0
#my_drive = odrive.find_any("serial:/dev/ttyUSB0")

##########print("resetting current mode to zero")
#missing code here
#my_drive.axis0.controller.pos_setpoint = 0 # stops


my_drive = odrive



my_drive.axis0.requested_state = CTRL_MODE_POSITION_CONTROL
my_drive.axis0.controller.pos_setpoint = 1500
print("changed mode to Position Control")
print("moved to position 1500")