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

def startDeniz(start_of_msg):
    
    startSequence = start_of_msg # add start_cache to beginning

    for i in range():  # there's 4 "chunks" of on/off sequences (11111)
        nextValue = None
        while startSequence[-1] == currentChunksBoolean: # while in current chunk
            nextValue = (chargetime() < CT_CUTOFF)  # read pulse
            time.sleep(S)
            startSequence.append(nextValue)         # add pulse to chunk
        currentChunksBoolean = not currentChunksBoolean #chunk is now opposite

    return startsequence

    ones=0
    zeros=0
    for i in start:
        if i:
            ones+=ones
        else:
            zeros+=zeros
    aveone = ones/10.
    avezero = zeros/10.
    return (aveone+avezero)/2.0

def ReadStartSequence(start_of_msg):
    """ Captures the known start sequence "11111000001111100000"
    for later analysis of the pulsewidth

    arguments:
        cache: initial part of the message, divided into 4 chunks 
        of 'True and False'

    returns:
        knownSampleHeader: the first part of the header, the known sample,
        as a boolean list 
    """
    startSequence = start_of_msg # add start_cache to beginning
    currentChunksBoolean = True

    for i in range(4):  # there's 4 "chunks" of on/off sequences (11111)
        nextValue = None
        while startSequence[-1] == currentChunksBoolean: # while in current chunk
            nextValue = (chargetime() < CT_CUTOFF)  # read pulse
            time.sleep(S)
            startSequence.append(nextValue)         # add pulse to chunk
        currentChunksBoolean = not currentChunksBoolean #chunk is now opposite

    return startsequence

def RyanStartSequence(start_of_msg):
    """ Captures the known start sequence (boolean list)"11111000001111100000"
    for later analysis of the pulse ewidth

    arguments:
        cache: initial part of the message, divided into 4 chunks 
        of 'True and False'

    returns:
        knownSampleHeader: the first part of the header, the known sample,
        as a boolean list 
    """
    startSequence = []
    workingframe = start_of_msg
    chunks = []

    while len(chunks) < 3:
        cutIndex = None
        while sum(workingframe)/len(workingframe) > .55:
            nextValue = (chargetime() < CT_CUTOFF)  # read pulse
            time.sleep(S)
            if workingframe[-1] != nextValue:
                cutIndex = workingframe.index(workingframe[-1])
            workingframe.append(nextValue)
        chunks.append(workingframe[:cutIndex])
        workingframe = workingframe[cutIndex:]
    # chunks probably look like [[True]*5*PW, [False]*5*PW, [True]*5*PW] and noise
    i = 1
    for chunk in chunks:
        print("length of chunk"+str(i)+":"+str(len(chunk))) 
        startSequence += chunk

    pwGuess = len(startSequence)/15
    print(pwGuess)

    # finish last Falses

    while len(workingframe) <= 5*pwGuess:# workingframe should be 5*PW
        workingframe.append(chargetime() < CT_CUTOFF)
        time.sleep(S)

    startSequence += workingframe
    pwGuess2 = len(startSequence)/20: 
    print("pwGuess2:",pwGuess2)
    if pwGuess == pwGuess2:
        return pwGuess
    else:
        print('ERROR: pwGuess does not match expectations')

##def dynamicaParseHeader(PW):
##    pass
##    cache = []
##    while len(cache) < 10*PW:
##        while True:
##            measurement = (chargetime() < CT_CUTOFF)
##            time.sleep(S)
##            currentChunksBoolean = cache[-1]
##            if not cache:                               # cache empty
##                cache.append(measurement)
##            elif currentChunksBoolean == measurement:   # still receiving consistent pattern
##                cache.append(measurement)
##            else:                                       # maybe new cache sequence?
##                measurement2 = (chargetime() < CT_CUTOFF)
##                time.sleep(S)
##                if measurement == measurement2:         # yes, new cache sequence!
##                    cachelength = len(cache)
##                    if cachelength % PW == 1: 
##                        if currentChunksBoolean == True:# a dot!
##                            morse += '.'
##                        else:                            # a symbol space                  
##                            continue
##                    elif cachelength % PW == 3:
##                        if currentChunksBoolean == True:# a dash!
##                            morse += '-'
##                        else:
##                    elif cachelength % PW == 




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

