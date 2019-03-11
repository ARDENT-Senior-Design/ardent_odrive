def myProcess():
	mode = "yes"
	if mode == "yes":
		#some code
		print ("mode equals 'yes'")
	elif mode == "no":
		#more code
		print ("mode equals 'no'")
	else:
		#last option
		print ("mode didn't equal yes or no.")

myProcess()

#User Interface
#def main(mode, userInput):
#def main():
	# modes: debug, user; 0, 1
	mode = 0
	debug = False
	userInput = input("What mode do you want?? ")
	while debug == False:
#			userInput = input("What mode do you want?? ")
#			print (userInput)
#			mode = userInput
#			print(mode)
		if userInput == 0:
			print ("This is now in Debug Mode")
			mode = userInput
#		elif userInput == 1:
#			mode = userInput
#			print ("This is now in User Mode")
		else:
			#print("error returning...")
			print ("That is not a valid entry, please enter 0 or 1")
			return

if __name__ == "__main__":
	main()
