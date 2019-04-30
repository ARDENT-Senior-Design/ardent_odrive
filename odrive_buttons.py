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
#		odrv0 = odrive.find_any()
#		print("found odrive")
#	else:
#		print("Not looking for ODrive")

# Defining stuff for main code
def configuration():
		# Calibrate motor and wait for it to finish
	print("configuring ODrive")
	# Velocity Tolerance Limit - disables the tolerance check for position control
	odrv0.axis0.controller.config.vel_limit_tolerance = 0.0
	# Motor Configuration - pole pairs = number of permanent magnets, not coils
	odrv0.axis0.motor.config.pole_pairs = 20
	# Encoder Counts Per Revolution - this is 4 times the PPR (assuming quadrature encoder)
	odrv0.axis0.encoder.config.cpr = 4000 # 4000 (decimal) and not 4096 (binary)
	# Velocity Limit - keeping this low for now, but the motor can go much higher
	odrv0.axis0.controller.config.vel_limit = 2000.0
	# Current Calibration
	odrv0.axis0.motor.config.calibration_current = 20.0  # changed from 20.0
	# Phase Inductance
	odrv0.axis0.motor.config.phase_inductance = 2.3983637220226228e-05
	# Phase Resistance
	odrv0.axis0.motor.config.phase_resistance = 0.058687932789325714
	# Current Limit - this is to protect the power supply
	odrv0.axis0.motor.config.current_lim = 5.0  # changed from 30.0
	# Encoder Configuration - setting encoder to use indexing
	odrv0.axis0.encoder.config.use_index = 0  # False b/c AS5047P index weird
	print("ODrive configured\n")

def calibration():  #class: stop
	# Find a connected ODrive (this will block until you connect one)
#	print("finding an odrive...")
#	odrv0 = odrive.find_any()
#	print("found odrive")
	print("starting calibration...")
	odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
	while odrv0.axis0.current_state != AXIS_STATE_IDLE:
	    time.sleep(0.1)
	print("full calibration sequence completed")

	odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
	print("defaulted to position control 'AXIS_STATE_CLOSED_LOOP_CONTROL'")
	print ("Calibration Completed\n")
	#main()

def posctrl():  #class: motion
	#print("odrv0.axis0.controller.config.control_mode = CTRL_MODE_POSITION_CONTROL")
	odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL  # seems like this is needed if last command was idle state
	time.sleep(.5)
	odrv0.axis0.controller.config.control_mode = CTRL_MODE_POSITION_CONTROL
	print("defaulted to position control 'CTRL_MODE_POSITION_CONTROL")
	time.sleep(.5)
	odrv0.axis0.controller.pos_setpoint = 10000
	print("position set to 10000")
	print("waiting...")
	time.sleep(2)  #this is wait time in seconds-assuming move from 0
	print("position at ~10000\n")
	#odrv0.axis0.requested_state = AXIS_STATE_IDLE  # not sure, seems that this is needed if another position command comes in after
	#main()

def velctrl():  #class: motion
	odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL  # seems like this is needed if last command was idle state
	time.sleep(.5)
	odrv0.axis0.controller.config.control_mode = CTRL_MODE_POSITION_CONTROL
	#print("odrv0.axis0.controller.config.control_mode = CTRL_MODE_VELOCITY_CONTROL")
	time.sleep(.5)
	odrv0.axis0.controller.pos_setpoint = -10000  # this doesn't seem to be working
	print("position set to -10000")
	print("waiting...")
	time.sleep(2)  #this is wait time in seconds-assuming move from 0
	print("position at ~-10000\n")
	#main()

def trajctrl():  #class: motion
	print("odrv0.axis0.controller.config.control_mode = CTRL_MODE_TRAJECTORY_CONTROL")

	#main()

def currentctrl():  #class: motion
	print("odrv0.axis0.controller.config.control_mode = CTRL_MODE_CURRENT_CONTROL")

	#main() 

def error():
	ctrlE = odrv0.axis0.controller.error
	motorE = odrv0.axis0.motor.error
	encoderE = odrv0.axis0.encoder.error
	if ctrlE == True:
		print("There is a controller error\n")
	elif motorE == True:
		print("There is a motor error\n")
	elif encoderE == True:
		print("There is an encoder error\n")
	else:
		print("No errors\n")

def idle():  #class: stop
	odrv0.axis0.requested_state = AXIS_STATE_IDLE
	#main()

def reset():  #class: stop
	bye()
	odrv0.reboot()

def count():
	print(odrv0.axis0.encoder.shadow_count)
	print("")

def restart():  #class: error
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

def calicheck():  #class: error
#if userInput == "calibration":
	cal = odrv0.axis0.motor.is_calibrated
	if cal == True:
		cal = True
		#print("Motor is calibrated")
		#main()
	else:
		cali = input("Motor not calibrated. Calibrate now (y/n)? ").lower()
		if cali == "y":
			#userInput = "0"
			print ("Now Calibrating")
			calibration()
		else:
			#userInput = "0"
			restart()
			#main()

def bye():
	print(" _                ")
	print("| |               ")
	print("| |__  _   _  ___ ")
	print("| '_ \| | | |/ _ \/")
	print("| |_) | |_| |  __/")
	print("|_.__/ \__, |\___|")
	print("        __/ |     ")
	print("       |___/      ")


def main():
	#userInput = askInput
	#while debug == True
		#userInput = input("What mode do you want? (ex: pos, vel, current, traj) ") - doesn't override
	while de == False:
		calicheck()
		userInput = input("What mode do you want? (ex: pos, vel) ").lower()
		if userInput == "s":  #if there's an or it gets stuck
			print ("Stopping Motor")
			idle()
			#restart()
			break
		elif userInput == "pos":
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
		elif userInput == "exit":  # this seems to need to be here instead of lower otherwise program loops at statement at this line
			bye()
			#reset()  # this means calibration is required after restart of script
			exit()
			break
		elif userInput == "calibration":
			calibration()
			main()
		elif userInput == "configuration":
			configuration()
			main()
		elif userInput == "error":
			error()
			main()
		elif userInput == "reset":
			reset()
		elif userInput == "count":
			count()
		elif userInput == "hi":
			print("Hello There! How are you?\n")
		elif userInput == "good":
			print("That's good to hear :D\n")						
		else:
			print ("That is not a valid entry, please try pos, vel, current, traj\n")
			#main()
			break




if __name__ == "__main__":
	print("finding an ODrive...")
	odrv0 = odrive.find_any()
	print("found odrive\n" )
	while debug == False:
		# Find a connected ODrive (this will block until you connect one)
		de = False
		#userInput = input("What mode do you want? (ex: pos, vel, current, traj) ")
		main()
	while debug == True:
		print("Not looking for ODrive\n")
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

   ---------------------------Window Object (Tkinter----------------------"""

"""---------------------------Archieve------------------------------------
mode = "0"
print("mode " + mode)
elif userInput == "reset" or "reboot":
	print("Rebooting ODrive")
	reset()

while odrv0.axis0.current_state != AXIS_STATE_IDLE:
    if userInput == "s":  #if there's an or it gets stuck
		print ("Stopping Motor")
		idle()

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
# optional classes added as comments to each def()
# now correctly shifts between each state (ex. pos, vel, s) - don't use the or (ie "stop" or "s")
# configuration at start taken out (assuming config already set)
# can check for controller, motor, and encoder errors
# added spaces after printouts for easy reading
# shadow_count added as count()
# can now reboot() odrive
# timing changed to .5 and 2 from 1.5 and 5 b/c reaching position is quick - no need to worry about command getting stopped prematurely
# .lower() everywhere? - make all lowercase
# changed to "odrv0" from "my_drive"
# can say "hi"
"""---------------------------Bug Fixes-----------------------------------"""

"""---------------------------Development---------------------------------"""
# spelling of control modes when switching to each
# prompt user for what value to change to specific pos/vel
# add velocity control (is currently just position a second time)
# while loop for calibration - notifies that calibration has completed (not before)
# be able to stop motor at anytime (multiple lines running at the same time)
# add workingwithHallppr.json to odrive_buttons.py's def configuration(): - right now is original, gains are off b/c optical

# odrive not found, retry? - loop needs to time-out
# main(userInput = input("What mode do you want? (ex: pos, vel, current, traj) ")) - haha figure this out
# write on pop up window instead of cmd
# integrate odrive_demo.py as well?
# reset input() variable instead of setting it to zero (goes to error if restarted from any mode)
# getting rid of unnecessary varables
"""---------------------------Development---------------------------------"""