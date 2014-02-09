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

    If something interesting is noticed (i.e. a '1'), we start paying attention by storing it in cache.

    If we continue to capture something interesting (measured by if the cache = [1, 1, 1]) as opposed
    to some noise (a random '1' amongst a list of '0's), 
    we know that a real message is now being received. 

    Return the initial part of the new message, so that capturing of the full message
    can begin.
    
    """

    cache = []

    while len(cache) < 3:   # exit loop when cache=[1,1,1] i.e. when a msg is coming through
        z = chargetime()
        if z < CT_CUTOFF:   
            cache.append(True)   # Something interesting! 
        else:               
            cache = []      # nothing interesting
        time.sleep(S)

    return cache            # return the inital part of the new incoming message

def CaptureMessage():
    """ Captures a message, a stops capturing after a period of False transmission

    return:
        binary: a binary list representing the transmission in it's oversampled form
    """
    
    cache = [True]*cache_size
    binary = []
                                        # general activity denoted by: [False]*cache_size
    while sum(cache)/cache_size > .02:  # break when general inactivity of false signals 

        z = (chargetime() < 100) and (cache[0])
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

