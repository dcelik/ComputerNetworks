"""
variables.py
------------
Author: Nick Francisci
Purpose: To provide one central location to store global variables for the program
Status: Tested and Working 2-17-14
"""


blink_time = .5;    #Time given to one blink for transmission
one_baud = int(1/blink_time);                   #Number of pulses required for transmission to occur at 1 baud
header_pulse = '11110';     #Binary string to indicate start of message according to CompNet Datalink Standards
stop_pulse = '10111010111010';                    #Binary string representing morse code "+" to establish where message ends according CompNet Datalink Standards
group_code = 'I';                                 #Single char representing transmission group code "I"
origin = 'N';                                     #Single char representing name of sender
dest = 'R';                                       #Single char representing name of recipient
func = 'A';                                       #Single char representing function of message
