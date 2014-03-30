import RPi.GPIO as GPIO
import time as time
from variables import *
global test
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
#allPackets = [];

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

def takeMeasurement(pin):
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,GPIO.LOW)
    GPIO.setup(pin,GPIO.IN)
    return bool(GPIO.input(pin))

def catchPacket(initialPacket,sending=False,stop_time=0):
    """
    Takes an initial packet (a tuple containing a value and duration e.g. [False,2]
    Returns a complete packet generated from raw data
    """
    start_time = 0
    if stop_time != 0:
        start_time = time.time()
    flag = False
    currentPacket = initialPacket
    while True:
        #print(".");
        if currentPacket[0]: #Deal with True packet
            if not sending: z = takeMeasurement(12)
            if sending: z = takeMeasurement(16)
            if z and not flag:  
                currentPacket = [True,currentPacket[1]+1]
            elif z and flag:
                currentPacket = [True,currentPacket[1]+2]
                flag = False
            elif not z and not flag:
                flag = True
            elif not z and flag:
                #print(currentPacket)
                #allPackets.append(currentPacket)
                return currentPacket

        else: #Deal with False packet
            if not sending: z = takeMeasurement(12)
            if sending: z = takeMeasurement(16)
            if not z and not flag:  
                currentPacket = [False,currentPacket[1]+1]
            elif not z and flag:
                currentPacket = [False,currentPacket[1]+2]
                flag = False
            elif z and not flag:
                flag = True
            elif z and flag:
                #print(currentPacket)
                #allPackets.append(currentPacket)
                return currentPacket
            if sending and time.time() >= (start_time+stop_time) and stop_time != 0:
                print('Returning none ' + str(start_time) + ' ' + str(time.time()))
                return None
        

def cleanPacket(packet,pulse_width):
    """
    Converts packets to binary strings
    """
    if packet[0]:
        if 0 <= packet[1] <= pulse_width*(1+tolerance):
            return "1"
        elif pulse_width*(3-tolerance) <= packet[1] <= pulse_width*(3+tolerance):
            return "111"
        else:
            return "1"
    elif not packet[0]:
        if 0 <= packet[1] <= pulse_width*(1+tolerance):
            return "0"
        elif pulse_width*(3-tolerance) <= packet[1] <= pulse_width*(3+tolerance):
            return "000"
        elif pulse_width*(7-tolerance) <= packet[1] <= pulse_width*(7+tolerance):
            return "0000000"
        elif packet[1] > pulse_width*(7+tolerance):
            return ""
        else:
            return "1"
            
def base36decode(number):
    """
    Converts base 36 numbers back into decimal numbers
    """
    return int(number, 36)

def catchAck(initialPacket,pulse_width):
    """
    Parses the acknowledgement
    """
    ack = ""
    binary = ""
    while len(ack) < 1:
        currentPacket = catchPacket(initialPacket,True)
        initialPacket = [not currentPacket[0],2]
        binary = binary + cleanPacket(currentPacket,pulse_width)
        if binary[-4:] == "1000" and binary[:-2] in binaryToCharDict:
            ack = ack + binaryToCharDict[binary[:-2]]
            binary = ""
        elif binary[-8:] == "10000000" and binary in binaryToCharDict:
            ack = ack + binaryToCharDict[binary]
            binary = ""
        elif binary[-4:] == "1000" and not binary[:-2] in binaryToCharDict or binary[-8:] == "10000000" and not binary in binaryToCharDict:
            ack = ack + "X"
            binary = ""
        
        
    return ack

def catchStartSequence(initialPacket, sending = False):
    # Catch start sequence
    startSequence = catchPacket(initialPacket, sending)
    initialPacket = [not startSequence[0],2]
    currentPacket = catchPacket(initialPacket, sending)
    initialPacket = [not currentPacket[0],2]
    #Actually get the message
    pulse_width = startSequence[1]/4
    return pulse_width

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
        if binary[-4:] == "1000" and binary[:-2] in binaryToCharDict:
            header = header + binaryToCharDict[binary[:-2]]
            binary = ""
        elif binary[-8:] == "10000000" and binary in binaryToCharDict:
            header = header + binaryToCharDict[binary]
            binary = ""
        elif binary[-4:] == "1000" and not binary[:-2] in binaryToCharDict or binary[-8:] == "10000000" and not binary in binaryToCharDict:
            header = header + "X"
            binary = ""
        
    #origin = header[0]
    #destination = header[1]
    #function = header[2]
    #length = header[3:]
    #print("Header received: " + header[0:3] + " " + str(base36decode(length)))
    #print("Origin: " + origin + ". Destination: " + destination )
    #print("Function: " + function + " Length: " + str(base36decode(length)))
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
        if binary[-4:] == "1000" and binary[:-2] in binaryToCharDict:
            message = message + binaryToCharDict[binary[:-2]]
            binary = ""
        elif binary[-8:] == "10000000" and binary[:-6] in binaryToCharDict:
            message = message + binaryToCharDict[binary[:-6]] + " "
            binary = ""
        elif binary == "1011101011101":
            message = message + "+"
        elif binary[-4:] == "1000" and not binary[:-2] in binaryToCharDict or binary[-8:] == "10000000" and not binary[:-6] in binaryToCharDict:
            message = message + "X"
            binary = ""

    #print("Message received:")
    #print(message[1:-1])
    #print(allPackets)
    return message
