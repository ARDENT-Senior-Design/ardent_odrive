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
my_drive.axis0.motor.config.calibration_current = 20.0  # changed from 20.0
# Phase Inductance
my_drive.axis0.motor.config.phase_inductance = 2.3983637220226228e-05
# Phase Resistance
my_drive.axis0.motor.config.phase_resistance = 0.058687932789325714
# Current Limit - this is to protect the power supply
my_drive.axis0.motor.config.current_lim = 30.0  # changed from 30.0
# Encoder Configuration - setting encoder to use indexing
my_drive.axis0.encoder.config.use_index = 1  # True

#my_drive.save_configuration()

print("odrive configured")

print("starting calibration...")
my_drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
while my_drive.axis0.current_state != AXIS_STATE_IDLE:
    time.sleep(0.1)
print("full calibration sequence completed")

# this works
my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
my_drive.axis0.controller.pos_setpoint = 1500
print("defaulted to position control 'AXIS_STATE_CLOSED_LOOP_CONTROL")
print("moved to position 1500")

# this doesn't seem to be working rn (2.13.2019, but not 2.18.2019)
# now it works, but needed to go to closed loop control then pos then vel ctrl
# noticed problems with back mounting flexing and encoder not straight
# this works now - just needed to activate closed loop control beforehand
#my_drive.axis0.controller.config.control_mode = CTRL_MODE_VELOCITY_CONTROL
#my_drive.axis0.controller.vel_setpoint = 1500
#print("defaulted to position control 'CTRL_MODE_VELOCITY_CONTROL")
#print("velocity set to 1500")

my_drive.axis0.controller.config.control_mode = CTRL_MODE_POSITION_CONTROL
my_drive.axis0.controller.pos_setpoint = 1500
print("defaulted to position control 'CTRL_MODE_POSITION_CONTROL")
print("position set to 1500")
print("waiting...")
time.sleep(1.5)  #this is wait time in secondsn-assuming move from 0
print("waited for 1")
my_drive.axis0.requested_state = AXIS_STATE_IDLE

#my_drive.axis0.requested_state = AXIS_STATE_IDLE
# each line is executed line by line, so if this comes right after pos_setpoint, the action doesn't complete

print("")
print("Please Manually Connect: 'sudo odrivetool shell'")
print("please select a control mode:")
print("- checking for errors: odrv0.axis0.controller.config.control_mode")
print("- example: odrv0.axis0.controller.config.control_mode = CTRL_MODE_POSITION_CONTROL (mode 3")
print("- example: odrv0.axis0.controller.config.control_mode = CTRL_MODE_VELOCITY_CONTROL (mode 2")
print("- example: odrv0.axis0.controller.config.control_mode = CTRL_MODE_CURRENT_CONTROL (mode 1)")
print("- example: odrv0.axis0.controller.config.control_mode = CTRL_MODE_VOLTAGE_CONTROL (mode 0)")


print("- checking for errors: odrv0.axis0.motor.is_calibrated")
print("- checking for errors: odrv0.axis0.motor.error")
print("-   note error is given in decimal --> convert to hex to find")
print("- checking for encoder: odrv0.axis0.encoder.shadow_count")
print("- checking for errors: hex(odrv0.axis0.encoder.error)")
print("-   note 0x30 is 0x10 | 0x20  (brake resistor unexpectedly disarmed + motor unexpectedly disarmed))")
print("- checking for errors: hex(odrv0.axis0.error)")
print("- checking for control mode: odrv0.axis0.controller.config.control_mode")