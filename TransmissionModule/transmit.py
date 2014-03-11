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
blink_time = variables.blink_time;      #Time given to one blink
one_baud = variables.one_baud;          #Number of blink times for one baud transmission
header_pulse = variables.header_pulse;  #Binary string to help establish pulse_width
stop_pulse = variables.stop_pulse;      #Binary string to establish where message ends
group_code = variables.group_code;      #Single char representing transmission group code
origin = variables.origin;              #Single char representing name of sender
dest = variables.dest;                  #Single char representing name of recipient
func = variables.func;                  #Single char representing function of message


#----Function Definitions----#
def blink(n=5,time=1):
    """
    A tester function to ensure that the pi is ready to send signals
    """
    
    for i in range(n):
        on()
        sleep(time)
        off()
        sleep(time)

def base36encode(number, alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    """Converts an integer to a base36 string."""
    if not isinstance(number, (int)):
        raise TypeError('number must be an integer')
 
    base36 = ''
    sign = ''
 
    if number < 0:
        sign = '-'
        number = -number
 
    if 0 <= number < len(alphabet):
        return sign + alphabet[number]
 
    while number != 0:
        number, i = divmod(number, len(alphabet))
        base36 = alphabet[i] + base36
 
    return sign + base36
 
def base36decode(number):
    return int(number, 36)
            
def sendMessage(message, verbose=False):
    """
    Sends a message from the user
    message = the message to be transmitted as a string
    """
    #Assemble LAN message to be sent at group speed
    length = str(base36encode(len(message))); #Length is measured in transmission characters
    if len(length) == 1:
        length = "0" + length
    message = translator.mess2Trans(message);
    subheader = origin + dest + func + length;
    subheader = translator.mess2Trans(subheader);
    LAN_trans = subheader + message;

    #Assemble start code, group code, and end code to be sent at standard speed
    g_c = translator.mess2Trans(group_code)
    STD_trans_start = header_pulse + g_c;
    STD_trans_stop = stop_pulse;
    
    if verbose:
        print("Transmitting message...");
        print("Your packaged message: " + translator.trans2Mess(g_c + LAN_trans))
        print("Your message as transmitted:")
        print("Sent at standard speed of " + str(one_baud*blink_time) + " dots per second:")
        print(STD_trans_start);
        print("Sent at group speed of " + str(1/blink_time) + " dots per second:");
        print(LAN_trans);
        #print("Sent at standard speed of " + str(one_baud*blink_time) + " dots per second:")
        print(STD_trans_stop);
    transmit(STD_trans_start, blink_time);
    transmit(LAN_trans, blink_time);
    transmit(STD_trans_stop, blink_time);

def transmit(trans,time):
    """
    A helper function for sendMessage that translates the message
    into actual blinks on the pi.
    trans = the message to be transmitted as a string of 1s and 0s
    """

    for i in range(len(trans)):
        if trans[i] == '1':
            on()
            sleep(time)
        else:
            off()
            sleep(time)
            
    off();
            

#----Executing Code----#
if __name__ == "__main__":
    print("Transmitter online...");
    print("Available functions: blink(), sendMessage(message)");
