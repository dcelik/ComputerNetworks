import RPi.GPIO as GPIO
import time as time

def takeMeasurment():
	""" Measures an LED blink with a photoresistor and returns
	True if it reads an "on" pulse for the measurement duration 
	and False for an "off" pulse.
	"""
	S = .1
	CUTOFF = 10

	ct=0

    GPIO.setup(12,GPIO.IN)

    while not GPIO.input(12):
        ct += 1

    GPIO.setup(12,GPIO.OUT)
    GPIO.output(12,GPIO.LOW)
    time.sleep(S)  
    
    return ct<CUTOFF

def catchPacket(initialPacket):
    currentPacket = initialPacket
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
            return currentPacket

    else: #Deal with False packet
        z = takeMeasurement()
        if not z and not flag:  
            currentPacket = [True,currentPacket[1]+1]
        elif not z and flag:
            currentPacket = [True,currentPacket[1]+2]
            flag = False
        elif z and not flag:
            flag = True
        elif z and flag:
            return currentPacket
