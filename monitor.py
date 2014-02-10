"""
Implements continous loop that reads in blinks and returns binary data as a list

author: rlouie
date: 2/5/14 15:30
"""


import RPi.GPIO as GPIO
import time as time
import translator as translator


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

RECIPIENT = 'Z' # Should be 'R' if monitor was running on Ryan's pi
S = .01
CT_CUTOFF = 7
cache_size = 250

def chargetime():
    ct=0

    GPIO.setup(12,GPIO.IN)

    while not GPIO.input(12):
        ct += 1

    GPIO.setup(12,GPIO.OUT)
    GPIO.output(12,GPIO.LOW)
    time.sleep(S)
    
    return ct

def chargetimes(n=100):
    return [chargetime() for i in range(n)]

def MonitorStartOfMsg():
    """ Determines if we've started receiving an actual transmission.

    If something interesting is noticed (i.e. a '1'), we start paying attention 
    by storing it in cache.

    If we continue to capture something interesting (measured by if the cache = [1, 1, 1]) 
    as opposed to some noise (a random '1' amongst a list of '0's), 
    we know that a real message is now being received. 

    Return the initial part of the new message, so that capturing of the full message
    can begin.
    
    """

    cache = []

    while len(cache) < 3:   # exit loop when cache=[True]*3 i.e. when a msg is coming through
        z = chargetime()
        if z < CT_CUTOFF:   # Something interesting!
            cache.append(True)    
        else:               # nothing interesting
            cache = []      
        time.sleep(S)

    return cache            # return the inital part of the new incoming message

def ReadKnownSampleHeader(start_of_msg):
    """ Captures the known sample header "111000111000" for later analysis of the pulsewidth

    arguments:
        cache: initial part of the message, divided into 4 chunks of 'True and False'

    returns:
        knownSampleHeader: the first part of the header, the known sample, as a boolean list 
    """
    knownSampleHeader = start_of_msg
    currentChunksBoolean = True

    for i in range(4):
        nextValue = None
        while knownSampleHeader[-1] == currentChunksBoolean:
            nextValue = (chargetime() < CT_CUTOFF)
        currentChunksBoolean = not currentChunksBoolean #invert currentChunksBoolean
        time.sleep(S)
        if i < 3: # do not append extra bits at the end of the known sample header
            knownSampleHeader.append(nextValue)

    return knownSampleHeader

def CaptureMessage():
    """ Captures a message, a stops capturing after a period of False transmission

    return:
        binary: a binary list representing the transmission in it's oversampled form
    """
    
    cache = [True]*cache_size
    binary = []
                                        # general activity denoted by: [False]*cache_size
    while sum(cache)/cache_size > .02:  # break when general inactivity of false signals 

        z = (chargetime() < CT_CUTOFF) and (cache[0])
        binary.append(z)
        
        cache.append(z)
        cache = cache[1:]   # update cache
        
        time.sleep(S)

    return binary

##def main():
##    print("Receiver Online...")
##    while True:
##        print("Listening for transmissions...")
##        start_of_msg = MonitorStartOfMsg()
##        print("Receiving transmission...")
##        binary = start_of_msg + CaptureMessage()
##        print("Transmission Received!")
##
##if __name__ == "__main__":
##    main()

