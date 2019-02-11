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
# Find an ODrive that is connected on the serial port /dev/ttyUSB0
#my_drive = odrive.find_any("serial:/dev/ttyUSB0")

# Calibrate motor and wait for it to finish
print("configuring odrive")
# Velocity Tolerance Limit - disables the tolerance check for position control
my_drive.axis0.controller.config.vel_limit_tolerance = 0.0
# Motor Configuration - pole pairs = number of ??
my_drive.axis0.motor.config.pole_pairs = 20
# Encoder Counts Per Revolution - this is half the encoder resolution due (1:2 ratio)
my_drive.axis0.encoder.config.cpr = 4096
# Velocity Limit - keeping this low for now, but the motor can go much higher
my_drive.axis0.controller.config.vel_limit = 2000.0
# Current Calibration
my_drive.axis0.motor.config.calibration_current = 20.0
# Phase Inductance
my_drive.axis0.motor.config.phase_inductance = 2.3983637220226228e-05
# Phase Resistance
my_drive.axis0.motor.config.phase_resistance = 0.058687932789325714
# Current Limit - this is to protect the power supply
my_drive.axis0.motor.config.current_lim = 30.0
# Encoder Configuration - setting encoder to use indexing
my_drive.axis0.encoder.config.use_index = 1
print("odrive configured")

print("starting calibration...")
my_drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
while my_drive.axis0.current_state != AXIS_STATE_IDLE:
    time.sleep(0.1)
print("full calibration sequence completed")

my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
print("defaulted to position control 'AXIS_STATE_CLOSED_LOOP_CONTROL")

print("")
print("Please Manually Connect: 'sudo odrivetool shell'")
print("please select a control mode:")
print("- example: odrv0.axis0.requested_state = CTRL_MODE_POSITION_CONTROL")
print("- example: odrv0.axis0.requested_state = CTRL_MODE_VELOCITY_CONTROL")
print("- example: odrv0.axis0.requested_state = CTRL_MODE_CURRENT_CONTROL")
print("- example: odrv0.axis0.requested_state = CTRL_MODE_VOLTAGE_CONTROL")
print("- checking for errors: hex(odrv0.axis0.error)")

#is there a way to check what control mode is active currently (know what to set to zero before switching to another mode)