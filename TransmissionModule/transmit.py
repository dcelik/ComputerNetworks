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
from catch import *
from random import uniform
from utilities import calc_checksum

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
        return sign + '0' + alphabet[number]
 
    while number != 0:
        number, i = divmod(number, len(alphabet))
        base36 = alphabet[i] + base36
        
    return sign + base36
 
def base36decode(number):
    return int(number, 36)
            
def sendMessage(destinationMAC='C', sourceMAC='A', payload='ICIAEEABCHELLO WORLD', verbose=False):
    """
    Sends a message from the user
    message = the message to be transmitted as a string
    """
    #Guardian against improper input
    if len(destinationMAC) != 1 or len(sourceMAC) != 1 or len(payload) < 7:
        return None
    
    #Assemble LAN message to be sent at group speed
    length = str(base36encode(len(payload))); #Length is measured in transmission characters

    payload_transmission = translator.mess2Trans(payload);
    MAC_header = destinationMAC + sourceMAC + length;
    checksum = calc_checksum(MAC_header + payload);
    MAC_header += checksum;
    MAC_header_transmission = translator.mess2Trans(MAC_header);
    LAN_trans = MAC_header_transmission + payload_transmission;

    #Assemble start code, group code, and end code to be sent at standard speed
    STD_trans_start = header_pulse;
    STD_trans_stop = stop_pulse;
    
    if verbose:
        print("Transmitting message...");
        print("Your packaged message: " + translator.trans2Mess(LAN_trans))
        print("Your message as transmitted:")
        print(LAN_trans);
    trials = 0
    while trials < 3:
        trials += 1;
        while True:
            packet = catchPacket([False,0],True,(1+uniform(0.4,0.6)))
            if packet == None:
                break
        transmit(STD_trans_start, blink_time);
        transmit(LAN_trans, blink_time);
        transmit(STD_trans_stop, blink_time);
        print("Done")
        wasReceived = receiveAck(destinationMAC);
        if wasReceived:
            print("Ack received.")
            return True
        else:
            print("Ack not received.")

    return False

def receiveAck(destination):
    initialPacket = [False,1]
    #Catch whitespace before ack
    print("one_step")
    currentPacket = catchPacket(initialPacket,True,1)
    if currentPacket == None: #If no ack received return False
        return False
    #Catch start sequence and determine pulse width
    initialPacket = [True,2]
    print("two_step")
    pulse_width = catchStartSequence(initialPacket, True)
    print("three_step")
    ack = catchAck([True,2],pulse_width)
    if ack == destination:
        return True
    else:
        return False


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
