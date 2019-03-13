#Import everything from tkinter
from tkinter import *
import time
import math

#Import from odrive
#from __future__ import print_function
import odrive
from odrive.enums import *
import time
import math

# Find a connected ODrive (this will block until you connect one)
print("finding an odrive...")
my_drive = odrive.find_any()
print("found odrive")

"""-----------------------------------------------------------------------"""
# Development:
# user input --> calibration, close etc
# 
# odrive not found, retry?
# write on pop up window instead of cmd
# integrate odrive_demo.py as well?
# reset input() variable instead of setting it to zero (goes to error if restarted from any mode)
# getting rid of unnecessary varables
"""-----------------------------------------------------------------------"""

"""-----------------------------------------------------------------------
# Create Window Object
#window=Tk()

#def closewindow():
#	exit()

#Define buttons
b1=Button(window,text="Calibration", width=12, command=calibration)
b1.grid(row=2,column=3)

b1=Button(window,text="Postion Control", width=12, command=posctrl)
b1.grid(row=3,column=3)

b1=Button(window,text="Velocity Control", width=12, command=velctrl)
b1.grid(row=4,column=3)

b1=Button(window,text="Trajectory Control", width=12, command=trajctrl)
b1.grid(row=5,column=3)

b1=Button(window,text="Current Control", width=12, command=currentctrl)
b1.grid(row=6,column=3)

b1=Button(window,text="Close", width=12, command=closewindow)
b1.grid(row=7,column=3)
b1.configure(text="Close")

#window.mainloop()

-----------------------------------------------------------------------"""


def calibration():
	# Find a connected ODrive (this will block until you connect one)
#	print("finding an odrive...")
#	my_drive = odrive.find_any()
#	print("found odrive")

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
	print("odrive configured")

	print("starting calibration...")
	my_drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
	while my_drive.axis0.current_state != AXIS_STATE_IDLE:
	    time.sleep(0.1)
	print("full calibration sequence completed")

	my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
	print("defaulted to position control 'AXIS_STATE_CLOSED_LOOP_CONTROL")

	my_drive.axis0.controller.config.control_mode = CTRL_MODE_POSITION_CONTROL
	print("defaulted to position control 'CTRL_MODE_POSITION_CONTROL")
	my_drive.axis0.controller.pos_setpoint = 1500
	print("position set to 1500")
	print("waiting...")
	time.sleep(1.5)  #this is wait time in seconds-assuming move from 0
	print("position at ~1500")
	print("position set to 0")
	print("waiting...")
	time.sleep(1.5)
	my_drive.axis0.controller.pos_setpoint = 0
	print("position at ~0")
	#my_drive.axis0.requested_state = AXIS_STATE_IDLE
	
	main()

"""-----------------------------------------------------------------------
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
-----------------------------------------------------------------------"""

def posctrl():
	print("my_drive.axis0.controller.config.control_mode = CTRL_MODE_POSITION_CONTROL")

	main()

def velctrl():
	print("my_drive.axis0.controller.config.control_mode = CTRL_MODE_VELOCITY_CONTROL")

	main()

def trajctrl():
	print("my_drive.axis0.controller.config.control_mode = CTRL_MODE_TRAJECTORY_CONTROL")

	main()

def currentctrl():
	print("my_drive.axis0.controller.config.control_mode = CTRL_MODE_CURRENT_CONTROL")

	main() 

def idle():
	print("my_drive.axis0.requested_state = AXIS_STATE_IDLE")

	main()

def restart():
	restart = input("Do you wish to restart (y/n)? ").lower()
	if restart == "y":
		userInput = "0"
		mode = "0"
	else:
		userInput = "0"
		mode = "0"
		exit()
"""-----------------------------------------------------------------------"""

def calicheck():
	calibration = my_drive.axis0.motor.is_calibrated
	print("hi")

def main():
	debug = False
	userInput = input("What mode do you want? (ex: pos, vel, current, traj) ")
	while debug == False:
		if userInput == "calibration":
			calicheck()  # so this doesn't work --> just put the 2 lines of code here
			if calibration == True:  # so this needs to be not in quotes
				print("Motor is already calibrated")
				main()
			else:
				print ("Now Calibrating")
				mode = "0"
				print("mode " + mode)

"""-----------------------------------------------------------------------"""

				#restart = input("Do you wish to restart (y/n)? ").lower()
				#restart = "y"
				#if restart == "y":
				#	userInput = "0"
				#	mode = "0"
				calibration()
				#else:
				#	userInput = "0"
				#	mode = "0"
				#	exit()
		elif userInput == "pos":
			print ("This is now in Position Control")
			mode = "1"
			print("mode " + mode)
			posctrl()
			restart()
		elif userInput == "vel":
			print ("This is now in Velocity Control")
			mode = "2"
			print("mode " + mode)
			velctrl()
			restart()
		elif userInput == "traj":
			print ("This is now in Trajectory Control")
			mode = "3"
			print("mode " + mode)
			trajctrl()
			restart()
		elif userInput == "current":
			print ("This is now in Current Control")
			mode = "4"
			print("mode " + mode)
			currentctrl()
			restart()
		elif userInput == "stop":
			print ("Stopping Motor")
			mode = "stop"
			print("mode " + mode)
			idle()
			restart()
		elif userInput == "exit" or "close":
			print ("Good Bye~~~")
			#mode = "stop"
			#print("mode " + mode)
			exit()
		else:
			print ("That is not a valid entry, please try pos, vel, current, traj")
			restart()




if __name__ == "__main__":
	main()
