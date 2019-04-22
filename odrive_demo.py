from __future__ import print_function

import odrive
from odrive.enums import *
import time
import math

# Find a ODrive (will wait until found)
print("finding an odrive...")
my_drive = odrive.find_any()

# Wait for Calibration to Finish
print("starting calibration...")
my_drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
while my_drive.axis0.current_state != AXIS_STATE_IDLE:
    time.sleep(0.1)
my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

# Reading from MCU (motor controller unit)
print("Bus voltage is " + str(my_drive.vbus_voltage) + "V")

# Changing Property Values and Printing the Change
my_drive.axis0.controller.pos_setpoint = 3.14
print("Position setpoint is " + str(my_drive.axis0.controller.pos_setpoint))

# Function Calls
#for i in [1,2,3,4]:
#    print('voltage on GPIO{} is {} Volt'.format(i, my_drive.get_adc_voltage(i)))

#userInput = input("What mode do you want? (ex: pos, vel, current, traj) ") - doesn't override
userInput = input("What position do you want? ")
print("Your desired position setpoint is " + userInput)
#my_drive.axis0.controller.pos_setpoint == userInput

# Demo Motion: incramental
if userInput <= 1000:
	div = 5
elif userInput >= 1000 & userInput < 5000:
	div = 10
elif userInput >= 5000 & userInput < 10000:
	div = 10
else:
	div = 100

setpoint = int(userInput) // div
print("goto " + str(int(setpoint)))
my_drive.axis0.controller.pos_setpoint = setpoint
time.sleep(0.01)

# Demo Motion: sine wave
t0 = time.monotonic()
while True:
    setpoint = 10000.0 * math.sin((time.monotonic() - t0)*2)  # returns the value (in fractional seconds) of a clock which never goes backwards
    print("goto " + str(int(setpoint)))
    my_drive.axis0.controller.pos_setpoint = setpoint
    time.sleep(0.01)




# Other

# Errors
	# Writing to Read-Only Property Values
my_drive.vbus_voltage = 11.0  # fails with `AttributeError: can't set attribute`
	# Writing Invalid Values
my_drive.motor0.pos_setpoint = "I like trains"  # fails with `ValueError: could not convert string to float`

# Configuration
# Calibrate motor and wait for it to finish
print("configuring ODrive")
# Velocity Tolerance Limit - disables the tolerance check for position control
my_drive.axis0.controller.config.vel_limit_tolerance = 0.0
# Motor Configuration - pole pairs = number of ??
my_drive.axis0.motor.config.pole_pairs = 20  ####################################################################################
# Encoder Counts Per Revolution - this is half the encoder resolution due (1:2 ratio)
my_drive.axis0.encoder.config.cpr = 4096 ####################################################################################
# Velocity Limit - keeping this low for now, but the motor can go much higher
my_drive.axis0.controller.config.vel_limit = 2000.0
# Current Calibration
my_drive.axis0.motor.config.calibration_current = 20.0  # changed from 20.0  ##########################################
# Phase Inductance
my_drive.axis0.motor.config.phase_inductance = 2.3983637220226228e-05
# Phase Resistance
my_drive.axis0.motor.config.phase_resistance = 0.058687932789325714
# Current Limit - this is to protect the power supply
my_drive.axis0.motor.config.current_lim = 30.0  # changed from 30.0 ###########################################################
# Encoder Configuration - setting encoder to use indexing
my_drive.axis0.encoder.config.use_index = 1  # True
print("ODrive configured")