"""
variables.py
------------
Author: Nick Francisci
Purpose: To provide one central location to store global variables for the program
Status: Tested and Working 2-17-14
"""


blink_time = .1;    #Time given to one blink for transmission
header_pulse = "11111000001111100000";  #Binary string to help establish pulse_width
stop_pulse = "11111111111";             #Binary string to establish where message ends
origin = 'N';                           #Single char representing name of sender
dest = 'R';                             #Single char representing name of recipient
func = '0001';                          #Function as a string reprentation of 4 numbers
