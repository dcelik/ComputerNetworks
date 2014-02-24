"""
transmit.py
-----------
Author: Nick Francisci
Purpose: To provide a user runnable class for sending
    messages from the pi.
Status: Tested and Working 2-17-14

"""

#----Imports and Setup----#
import RPi.GPIO as GPIO
from time import sleep
import translator as translator
import variables as variables

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)

def on(): GPIO.output(7,True)
def off(): GPIO.output(7,False)


#----Import Global Variables----#
s = variables.blink_time;               #Time given to one blink
header_pulse = variables.header_pulse;  #Binary string to help establish pulse_width
stop_pulse = variables.stop_pulse;      #Binary string to establish where message ends
group_code = variables.group_code;      #Single char representing transmission group code
origin = variables.origin;              #Single char representing name of sender
dest = variables.dest;                  #Single char representing name of recipient
func = variables.func;                  #Single char representing function of message


#----Function Definitions----#
def blink(n=5):
    """
    A tester function to ensure that the pi is ready to send signals
    """
    
    for i in range(n):
        on()
        sleep(s)
        off()
        sleep(s)


            
def sendMessage(message, verbose=False):
    """
    Sends a message from the user
    message = the message to be transmitted as a string
    """
    
    message = translator.mess2Trans(message);
    length = str(len(message)); #Length is measured in transmission characters
    subheader = origin + dest + func + length;
    subheader = translator.mess2Trans(subheader);

    #Assemble Message  
    trans = header_pulse + group_code + subheader + message + stop_pulse;
    print("Transmitting message...");
    if verbose:
        print("Your packaged message: " + translator.trans2Mess(subheader + message))
        print("Your message as transmitted: " + trans)
    transmit(trans)

def transmit(trans):
    """
    A helper function for sendMessage that translates the message
    into actual blinks on the pi.
    trans = the message to be transmitted as a string of 1s and 0s
    """

    for i in range(len(trans)):
        if trans[i] == '1':
            on()
            sleep(s)
        else:
            off()
            sleep(s)
            
    off();
            

#----Executing Code----#
if __name__ == "__main__":
    print("Transmitter online...");
    print("Available functions: blink(), sendMessage(message)");
