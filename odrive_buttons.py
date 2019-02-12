#Import everything from tkinter
from tkinter import *

#from __future__ import print_function
#import odrive
#from odrive.enums import *
import time
import math

"""-----------------------------------------------------------------------"""
#Create Window object
window=Tk()

def closewindow():
	exit()

def calibration():
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

	print("starting calibration...")
	my_drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

def posctrl():
	print("odrv0.axis0.requested_state = CTRL_MODE_POSITION_CONTROL")
def velctrl():
	print("odrv0.axis0.requested_state = CTRL_MODE_VELOCITY_CONTROL")
def trajectoryctrl():
	print("odrv0.axis0.requested_state = CTRL_MODE_TRAJECTORY_CONTROL")
def currentctrl():
	print("odrv0.axis0.requested_state = CTRL_MODE_CURRENT_CONTROL")

"""-----------------------------------------------------------------------"""
#Define buttons
b1=Button(window,text="Calibration", width=12, command=calibration)
b1.grid(row=2,column=3)

b1=Button(window,text="Postion Control", width=12, command=posctrl)
b1.grid(row=3,column=3)

b1=Button(window,text="Velocity Control", width=12, command=velctrl)
b1.grid(row=4,column=3)

b1=Button(window,text="Trajectory Control", width=12, command=trajectoryctrl)
b1.grid(row=5,column=3)

b1=Button(window,text="Current Control", width=12, command=currentctrl)
b1.grid(row=6,column=3)

b1=Button(window,text="Close", width=12, command=closewindow)
b1.grid(row=7,column=3)
b1.configure(text="Close")

window.mainloop()