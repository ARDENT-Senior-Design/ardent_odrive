#User Interface

#def main(mode, userInput):
def main():
	debug = False
	userInput = input("What mode do you want?? ")
	while debug == False:
		if userInput == "0":
			print ("This is now in Debug Mode")
			mode = userInput
			#print(mode)
			restart = input("Do you wish to restart (y/n)? ").lower()
			if restart == "y":
				main()
			else:
				exit()
		elif userInput == "1":
			print ("This is now in User Mode")
			mode = userInput
			#print(mode)
			restart = input("Do you wish to restart (y/n)? ").lower()
			if restart == "y":
				main()
			else:
				exit()
		else:
			print ("That is not a valid entry, please enter 0 or 1")
			restart = input("Restart (y/n)? ").lower()
			if restart == "y":
				main()
			else:
				exit()

if __name__ == "__main__":
	main()