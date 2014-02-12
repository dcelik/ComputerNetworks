"""
readStartSequence(start_of_msg)
INPUTS: takes the start of message captured by the monitor function
OUTPUTS: returns the pulse width
"""

#import RPi.GPIO as GPIO
import time as time

def takeMeasurement():
    ct=0

    GPIO.setup(12,GPIO.IN)

    while not GPIO.input(12):
        ct += 1

    GPIO.setup(12,GPIO.OUT)
    GPIO.output(12,GPIO.LOW)

    if ct < 100:
        return True
    else:
        return False


def readStartSequence(start_of_msg):
    pause = .01
    pwPreHypothesis = 0
    binaryCache = start_of_msg
    for n in range(2)
        while binaryCache[-1] == True:
            status = takeMeasurement()
            binaryCache.append(status)
            time.sleep(pause)
        if binaryCache <= 3:
            print("ERROR pulse width too small")
        pwPreHypothesis += len(binaryCache)-1
        binaryCache = [False]
        if n != 2:
            while binaryCache[-2:] != [True,True]
                status = takeMeasurement()
                binaryCache.append(status)
                time.sleep(pause)
        else:
            time.sleep(pause*pwHypothesis*5)
        pwPreHypothesis += len(binaryCache)-2
        binaryCache = [True,True]
        pwHypothesis = pwPreHypothesis/10.0
    pwHypothesis = pwPreHypothesis/15.0
    return int(round(pwHypothesis))
        
