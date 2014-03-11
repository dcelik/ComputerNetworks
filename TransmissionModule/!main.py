"""
main.py
-------
Author: Ian, Nick, Deniz, and Ryan
Purpose: To provide one central user UI function to run all of the program
Status: Tested and Working 2-17-14

"""

#----Imports and Setup----#
from transmit import sendMessage, on, off
from receive import receiveMessage
import variables



#----Functions----#
def main():
    #Display list of functions available to user (keep these as few as possible)
    print("Available functions: sendMessage(message),receiveMessage()")

    #Need to Implement: Working monitor function boiled down to one user runnable function

#----Running Code----#
if __name__ == "__main__":
    main()


