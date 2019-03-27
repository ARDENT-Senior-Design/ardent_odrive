
#!/usr/bin/env python

#Import ros pacakges
import rospy
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

# Defining stuff for main code
def calibration():
	# Find a connected ODrive (this will block until you connect one)
#	print("finding an odrive...")
#	my_drive = odrive.find_any()
#	print("found odrive")

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
	
	#main()

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
	#main()

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
	#main()

def trajctrl():
	print("my_drive.axis0.controller.config.control_mode = CTRL_MODE_TRAJECTORY_CONTROL")

	#main()

def currentctrl():
	print("my_drive.axis0.controller.config.control_mode = CTRL_MODE_CURRENT_CONTROL")

	#main() 

def idle():
	my_drive.axis0.requested_state = AXIS_STATE_IDLE

	#main()

def reset():
	my_drive.reboot()

def restart():
	restart = input("Do you wish to restart (y/n)? ").lower()
	if restart == "y":
		#userInput = "0" - doesn't work
		#userInput = input("What mode do you want? (ex: pos, vel, current, traj) ") - doesn't override
		#userInput = input("something else") - doesn't override either
		#debug = True
		main()
	else:
		#userInput = "0" - doesn't work
		#userInput = input("What mode do you want? (ex: pos, vel, current, traj) ") - doesn't override
		exit()

def calicheck():
#if userInput == "calibration":
	cal = my_drive.axis0.motor.is_calibrated
	if cal == True:
		print("Motor is calibrated")
		#main()
	else:
		cali = input("Motor not calibrated. Calibrate now (y/n)? ").lower()
		if cali == "y":
			#userInput = "0"
			print ("Now Calibrating")
			calibration()
			print ("Calibration Completed")
		else:
			#userInput = "0"
			main()

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

def main():
	#userInput = askInput
	#while debug == True
		#userInput = input("What mode do you want? (ex: pos, vel, current, traj) ") - doesn't override
    rospy.init_node('odrive', anonymous=True)
	rospy.Subscriber("chatter", String, updateSetpoints)
	pub = rospy.Publisher('chatter', String, queue_size=10)

	while de == False:
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
			main()
		elif userInput == "stop" or "s":
			print ("Stopping Motor")
			idle()
			#restart()
			break
		else:
			print ("That is not a valid entry, please try pos, vel, current, traj")
			#main()
			break
		rospy.spin()




if __name__ == "__main__":
	print("finding an ODrive...")
	my_drive = odrive.find_any()
	print("found odrive")
	while debug == False:
		# Find a connected ODrive (this will block until you connect one)
		de = False
		#userInput = input("What mode do you want? (ex: pos, vel, current, traj) ")
		main()
	while debug == True:
		print("Not looking for ODrive")
		de = False
		exit()
	#userInput = input("What mode do you want? (ex: pos, vel, current, traj) ")
	#main()


"""---------------------------Window Object (Tkinter)---------------------
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

   ---------------------------Window Object (Tkinter)---------------------"""

"""---------------------------Archieve------------------------------------
mode = "0"
print("mode " + mode)
elif userInput == "reset" or "reboot":
	print("Rebooting ODrive")
	reset()
   ---------------------------Archieve------------------------------------"""

"""---------------------------ODrive Notes--------------------------------
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
   ---------------------------ODrive Notes--------------------------------"""

"""---------------------------Bug Fixes-----------------------------------"""
# fix moving to multiple positions
# check if calibrated at each mode - if not, prompt to calibrate
# reset userInput so it doesn't loop - was becauuse value stays when in a while loop, used break, reprompted, re-entered loop, fixed
# when userInput = "exit" --> Motor is Calibrated --> why? --> position of userInput=exit is 5th instead of lower otherwise program loops at statement at that line
# put calicheck() back at each mode - rn if not calibrated, will calibrate, return and do the mode switch twice (pos ctrl and pos ctrl) --> had main() at end of calibration()
"""---------------------------Bug Fixes-----------------------------------"""

"""---------------------------Development---------------------------------"""
# spelling of control modes when switching to each
# .lower() everywhere?
# prompt user for what value to change to specific pos/vel
# while loop for calibration - notifies that calibration has completed (not before)
 
# odrive not found, retry?
# main(userInput = input("What mode do you want? (ex: pos, vel, current, traj) ")) - haha figure this out
# write on pop up window instead of cmd
# integrate odrive_demo.py as well?
# reset input() variable instead of setting it to zero (goes to error if restarted from any mode)
# getting rid of unnecessary varables
"""---------------------------Development---------------------------------"""
