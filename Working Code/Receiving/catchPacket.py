"""
takeMeasurement.py
"""

def takeMeasurment():
	""" Measures an LED blink with a photoresistor and returns
	True if it reads an "on" pulse for the measurement duration 
	and False for an "off" pulse.
	"""
	S = .01
	CUTOFF = 10

	ct=0

    GPIO.setup(12,GPIO.IN)

    while not GPIO.input(12):
        ct += 1

    GPIO.setup(12,GPIO.OUT)
    GPIO.output(12,GPIO.LOW)
    time.sleep(S)  
    
    return ct<CUTOFF
