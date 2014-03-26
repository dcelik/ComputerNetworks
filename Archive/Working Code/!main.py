import RPi.GPIO as GPIO
import time as time
import math
import takeMeasurement.takeMeasurement as takeMeasurement


import translator as translator
from NIRDreceive import pause
import math

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

def main():
    print("Receiver Online...")
    while True:
        print("Listening for transmissions...")
        start_of_msg = MonitorStartOfMsg()
        print("Receiving transmission...")
        print(start_of_msg)
        #pwidth = readStartSequence(start_of_msg)
        pwidth = startDeniz(start_of_msg)
        print(pwidth)
        header = dynamicParseHeader(pwidth)
        print(header)
        message = dynamicParseMessage(pwidth,header)
        #remaining_binary_message = CaptureMessage()
        print("Transmission Received!")
        print("Pulse width = " + str(pwidth))
        print("Message = " + message)
        #consolidated = consolidate(known_sample_header+remaining_binary_message, pwidth)
        #print(consolidated)
        #print(trans2Mess(''.join([fromBoolean(d) for d in consolidated])))
        

def fromBoolean(d):
    if d:
        return '1'
    else:
        return '0'

def toBool(d):
    if d=='1':
        return True;
    else:
        return False;

if __name__ == "__main__":
    main()


