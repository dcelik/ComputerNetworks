import RPi.GPIO as GPIO
from time import sleep
import translator as translator

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)


def on(): GPIO.output(7,True)
def off(): GPIO.output(7,False)

s = .1 #Set in conjuction with ReadBlink entry_time

def blink(n=5):
    for i in range(n):
        on()
        sleep(s)
        off()
        sleep(s)

def transmit(trans):
    for i in range(len(trans)):
        if trans[i] == '1':
            on()
            sleep(s)
        else:
            off()
            sleep(s)

print("Transmitter online...")
