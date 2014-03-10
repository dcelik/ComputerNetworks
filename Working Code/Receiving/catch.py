import RPi.GPIO as GPIO
import time as time
from variables import *
global test

# The means of testing it without a pi
##test = -1
##testPackets = [[False, 200], [True, 40], [False, 10], [True, 10], [False, 10], [True, 10], [False, 30], [True, 30], [False, 10], [True, 10], [False, 30], [True, 10], [False, 10], [True, 30], [False, 10], [True, 10], [False, 30], [True, 10], [False, 10], [True, 30], [False, 30], [True, 30], [False, 10], [True, 30], [False, 10], [True, 30], [False, 10], [True, 30], [False, 10], [True, 30], [False, 30], [True, 10], [False, 10], [True, 30], [False, 10], [True, 10], [False, 30], [True, 30], [False, 30], [True, 10], [False, 10], [True, 10], [False, 10], [True, 10], [False, 10], [True, 10], [False, 30], [True, 10], [False, 10], [True, 10], [False, 30], [True, 10], [False, 10], [True, 10], [False, 10], [True, 10], [False, 70], [True, 10], [False, 10], [True, 10], [False, 30], [True, 10], [False, 10], [True, 10], [False, 10], [True, 10], [False, 70], [True, 10], [False, 10], [True, 30], [False, 70], [True, 10], [False, 10], [True, 30], [False, 10], [True, 10], [False, 10], [True, 10], [False, 30], [True, 30], [False, 10], [True, 30], [False, 10], [True, 30], [False, 30], [True, 30], [False, 10], [True, 10], [False, 30], [True, 30], [False, 10], [True, 30], [False, 10], [True, 10], [False, 70], [True, 30], [False, 30], [True, 10], [False, 30], [True, 10], [False, 10], [True, 10], [False, 10], [True, 10], [False, 30], [True, 30], [False, 70], [True, 30], [False, 10], [True, 30], [False, 30], [True, 10], [False, 30], [True, 10], [False, 10], [True, 10], [False, 10], [True, 10], [False, 30], [True, 10], [False, 10], [True, 10], [False, 10], [True, 10], [False, 30], [True, 10], [False, 10], [True, 30], [False, 30], [True, 30], [False, 10], [True, 30], [False, 10], [True, 10], [False, 30], [True, 10], [False, 30], [True, 10], [False, 10], [True, 30], [False, 10], [True, 10], [False, 10], [True, 30], [False, 10], [True, 10]]
##testPackets = testPackets + testPackets

#----Functions for taking raw data----#
##def takeMeasurement():
##    """ Measures an LED blink with a photoresistor and returns
##    True if it reads an "on" pulse for the measurement duration 
##    and False for an "off" pulse.
##    """
##    S = .1
##    CUTOFF = 10
##
##    ct=0
##
##    GPIO.setup(12,GPIO.IN)
##
##    while not GPIO.input(12):
##        ct += 1
##
##    GPIO.setup(12,GPIO.OUT)
##    GPIO.output(12,GPIO.LOW)
##    time.sleep(S)  
##    
##    return ct<CUTOFF

def takeMeasurement():
    S = 0.1
    GPIO.setup(12,GPIO.OUT)
    GPIO.output(12,GPIO.LOW)
    sleep(s)
    GPIO.setup(12,GPIO.IN)
    return bool(GPIO.input(12))

def catchPacket(initialPacket):
    """
    Takes an initial packet (a tuple containing a value and duration e.g. [False,2]
    Returns a complete packet generated from raw data
    """
    flag = False
    currentPacket = initialPacket
    while True:
        if currentPacket[0]: #Deal with True packet
            z = takeMeasurement()
            if z and not flag:  
                currentPacket = [True,currentPacket[1]+1]
            elif z and flag:
                currentPacket = [True,currentPacket[1]+2]
                flag = False
            elif not z and not flag:
                flag = True
            elif not z and flag:
                print(currentPacket)
                return currentPacket

        else: #Deal with False packet
            z = takeMeasurement()
            if not z and not flag:  
                currentPacket = [False,currentPacket[1]+1]
            elif not z and flag:
                currentPacket = [False,currentPacket[1]+2]
                flag = False
            elif z and not flag:
                flag = True
            elif z and flag:
                print(currentPacket)
                return currentPacket
        
##def catchPacket(initialPacket):
##    """ This is the test function """
##    global test
##    test += 1
##    if test < len(testPackets):
##        return testPackets[test]

def cleanPacket(packet,pulse_width):
    """
    Converts packets to binary strings
    """
    if packet[0]:
        if pulse_width*.5 <= packet[1] <= pulse_width*1.5:
            return "1"
        elif pulse_width*2.5 <= packet[1] <= pulse_width*3.5:
            return "111"
        else:
            print("Packet error!")
            print(packet)
    elif not packet[0]:
        if pulse_width*.5 <= packet[1] <= pulse_width*1.5:
            return "0"
        elif pulse_width*2.5 <= packet[1] <= pulse_width*3.5:
            return "000"
        elif pulse_width*6 <= packet[1] <= pulse_width*8:
            return "0000000"
        elif packet[1] > pulse_width*8:
            return ""
        else:
            print("Packet error!")
            print(packet)
            
def base36decode(number):
    """
    Converts base 36 numbers back into decimal numbers
    """
    return int(number, 36)
        
def catchHeader(initialPacket, pulse_width):
    """
    Parses the packets that make up the header and returns that information to the user
    """
    header = ""
    binary = ""
    while len(header) < 6:
        currentPacket = catchPacket(initialPacket)
        initialPacket = [not currentPacket[0],2]
        binary = binary + cleanPacket(currentPacket,pulse_width)
        if binary[-4:] == "1000":
            header = header + binaryToCharDict[binary[:-2]]
            binary = ""
            print(header)
        if binary[-8:] == "10000000":
            header = header + binaryToCharDict[binary]
            binary = ""
            print(header)
        
    group_code = header[0]
    origin = header[1]
    destination = header[2]
    function = header[3]
    length = header[4:]
    print("Header received.")
    print("Group code: " + group_code + ". Origin: " + origin + ". Destination: " + destination )
    print("Function: " + function + " Length: " + str(base36decode(length)))
    return header

def catchMessage(initialPacket, pulse_width):
    """
    Parses the packets that make up the message and returns the message to the user
    """
    message = " "
    binary = ""
    while message[-1] != "+":
        currentPacket = catchPacket(initialPacket)
        initialPacket = [not currentPacket[0],2]
        binary = binary + cleanPacket(currentPacket, pulse_width)
        if binary[-4:] == "1000":
            message = message + binaryToCharDict[binary[:-2]]
            binary = ""
        elif binary[-8:] == "10000000":
            message = message + binaryToCharDict[binary[:-6]] + " "
            binary = ""
        elif binary == "1011101011101":
            message = message + "+"

    print("Message received:")
    print(message[1:-1])
    return message
