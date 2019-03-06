#!/usr/bin/env python3
"""
ODrive Calibration Sequance
"""
from __future__ import print_function

import odrive
from odrive.enums import *
import time
import math

# Find a connected ODrive (this will block until you connect one)
print("finding an odrive...")
my_drive = odrive.find_any()
print("found odrive")

#print("starting calibration...")
#my_drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
#while my_drive.axis0.current_state != AXIS_STATE_IDLE:
#    time.sleep(0.1)
#print("full calibration sequence completed")

my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
#print("defaulted to position control 'AXIS_STATE_CLOSED_LOOP_CONTROL")
my_drive.axis0.controller.config.control_mode = CTRL_MODE_VELOCITY_CONTROL
print("set to 'CTRL_MODE_VELOCITY_CONTROL")
my_drive.axis0.controller.vel_setpoint = 0
print("waiting for 1.5 seconds...")
time.sleep(1.5)  #this is wait time in secondsn-assuming move from 0
#print("waited for 1.5 seconds")
#print("stopped at " + my_drive.axis0.encoder.shadow_count) # doesn't work
print("stopped at encoder position")
print(my_drive.axis0.encoder.shadow_count)
my_drive.axis0.requested_state = AXIS_STATE_IDLE