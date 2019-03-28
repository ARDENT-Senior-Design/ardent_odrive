#!/usr/bin/env python

#Import ros pacakges
import rospy

#import standard libraries
import time
import math
import logging
import traceback

#Import from odrive
#from __future__ import print_function
import odrive
from odrive.enums import *


debug = False  # set this before running the code
#askInput = input("What mode do you want? (ex: pos, vel, current, traj) ")


#def debug():
#	if debug == False:
#		# Find a connected ODrive (this will block until you connect one)
#		print("finding an ODrive...")
#		my_drive = odrive.find_any()
#		print("found odrive")
#	else:
#		print("Not looking for ODrive")

# Defining stuff for run_odrive code
def calibration():
	# Find a connected ODrive (this will block until you connect one)
	# print("finding an odrive...")
	# my_drive = odrive.find_any()
	# print("found odrive")

	# Calibrate motor and wait for it to finish
	print("configuring ODrive")
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
	print("ODrive configured")

	print("starting calibration...")
	my_drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
	while my_drive.axis0.current_state != AXIS_STATE_IDLE:
	    time.sleep(0.1)
	print("full calibration sequence completed")

	my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
	print("defaulted to position control 'AXIS_STATE_CLOSED_LOOP_CONTROL'")
	
	#run_odrive()

def posctrl():
	#print("my_drive.axis0.controller.config.control_mode = CTRL_MODE_POSITION_CONTROL")
	my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL  # seems like this is needed if last command was idle state
	time.sleep(1.5)
	my_drive.axis0.controller.config.control_mode = CTRL_MODE_POSITION_CONTROL
	print("defaulted to position control 'CTRL_MODE_POSITION_CONTROL")
	time.sleep(1.5)
	my_drive.axis0.controller.pos_setpoint = 1500
	print("position set to 1500")
	print("waiting...")
	time.sleep(5)  #this is wait time in seconds-assuming move from 0
	print("position at ~1500")
	#my_drive.axis0.requested_state = AXIS_STATE_IDLE  # not sure, seems that this is needed if another position command comes in after
	#run_odrive()

def velctrl():
	my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL  # seems like this is needed if last command was idle state
	time.sleep(1.5)
	my_drive.axis0.controller.config.control_mode = CTRL_MODE_POSITION_CONTROL
	#print("my_drive.axis0.controller.config.control_mode = CTRL_MODE_VELOCITY_CONTROL")
	time.sleep(1.5)
	my_drive.axis0.controller.pos_setpoint = 0  # this doesn't seem to be working
	print("position set to 0")
	print("waiting...")
	time.sleep(5)  #this is wait time in seconds-assuming move from 0
	print("position at ~0")
	#run_odrive()

def trajctrl():
	print("my_drive.axis0.controller.config.control_mode = CTRL_MODE_TRAJECTORY_CONTROL")

	#run_odrive()

def currentctrl():
	print("my_drive.axis0.controller.config.control_mode = CTRL_MODE_CURRENT_CONTROL")

	#run_odrive() 

def idle():
	my_drive.axis0.requested_state = AXIS_STATE_IDLE

	#run_odrive()

def reset():
	my_drive.reboot()

def restart():
	restart = input("Do you wish to restart (y/n)? ").lower()
	if restart == "y":
		#userInput = "0" - doesn't work
		#userInput = input("What mode do you want? (ex: pos, vel, current, traj) ") - doesn't override
		#userInput = input("something else") - doesn't override either
		#debug = True
		run_odrive()
	else:
		#userInput = "0" - doesn't work
		#userInput = input("What mode do you want? (ex: pos, vel, current, traj) ") - doesn't override
		exit()

def calicheck():
#if userInput == "calibration":
	cal = my_drive.axis0.motor.is_calibrated
	if cal == True:
		print("Motor is calibrated")
		#run_odrive()
	else:
		cali = input("Motor not calibrated. Calibrate now (y/n)? ").lower()
		if cali == "y":
			#userInput = "0"
			print ("Now Calibrating")
			calibration()
			print ("Calibration Completed")
		else:
			#userInput = "0"
			run_odrive()

def bye():
	print(" _                ")
	print("| |               ")
	print("| |__  _   _  ___ ")
	print("| '_ \| | | |/ _ \/")
	print("| |_) | |_| |  __/")
	print("|_.__/ \__, |\___|")
	print("        __/ |     ")
	print("       |___/      ")

def updateSetpoints():
	print("I have updated the setpoints.")

def run_odrive():
	rospy.init_node('odrive')
	#userInput = askInput
	#while debug == True
	#userInput = input("What mode do you want? (ex: pos, vel, current, traj) ") - doesn't override
	main_rate = rospy.Rate(100) # hz        
	# Start timer to run high-rate comms
	fast_timer = rospy.Timer(rospy.Duration(1/float(odom_calc_hz)), fast_timer)
	while not rospy.is_shutdown():
		calicheck()
		userInput = input("What mode do you want? (ex: pos, vel, current, traj) ")
		if userInput == "pos":
			calicheck()
			print ("Now in Position Control")
			posctrl()
			#restart()
			#debug = True
			break
		elif userInput == "vel":
			calicheck()
			print ("Now in Velocity Control")
			velctrl()
			#restart()
			break
		elif userInput == "traj":
			calicheck()
			print ("Now in Trajectory Control")
			trajctrl()
			#restart()
			break
		elif userInput == "current":
			calicheck()
			print ("Now in Current Control")
			currentctrl()
			#restart()
			break
		elif userInput == "exit" or "leave":  # this seems to need to be here instead of lower otherwise program loops at statement at this line
			bye()
			#reset()  # this means calibration is required after restart of script
			exit()
			break
		elif userInput == "calibration" or "cali":
			calicheck()
		elif userInput == "stop" or "s":
			print ("Stopping Motor")
			idle()
			#restart()
			break
		else:
			print ("That is not a valid entry, please try pos, vel, current, traj")
			break
		rospy.spin()




if __name__ == "__main__":
	print("finding an ODrive...")
	my_drive = odrive.find_any()
	print("found odrive")
	if debug == False:
		# Find a connected ODrive (this will block until you connect one)
		de = False
		#userInput = input("What mode do you want? (ex: pos, vel, current, traj) ")
		run_odrive()
	else:
		print("Not looking for ODrive")
		de = False
		exit()
	#userInput = input("What mode do you want? (ex: pos, vel, current, traj) ")
	#main()
