"""
variables.py
------------
Author: Nick Francisci
Purpose: To provide one central location to store global variables for the program
Status: Tested and Working 2-17-14
"""


blink_time = .1;    #Time given to one blink for transmission
one_baud = int(1/blink_time);                     #Number of pulses required for transmission to occur at 1 baud
header_pulse = "1"*4*one_baud + "0"*one_baud;       #Binary string to indicate start of message according to CompNet Datalink Standards
ob_dot = "1"*one_baud + "0"*one_baud;
ob_dash = "1"*3*one_baud + "0"*one_baud;
stop_pulse = ob_dot + ob_dash + ob_dot + ob_dash + ob_dot;   #Binary string representing morse code "+" to establish where message ends according CompNet Datalink Standards
group_code = ob_dot + ob_dot + "0"*2*one_baud;    #Binary string representing transmission group code "I"
origin = 'N';                                     #Single char representing name of sender
dest = 'R';                                       #Single char representing name of recipient
func = 'A';                                       #Single char representing function of message
