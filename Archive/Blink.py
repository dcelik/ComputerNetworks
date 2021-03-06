import RPi.GPIO as GPIO
from time import sleep
import translator as translator

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)


def on(): GPIO.output(7,True)
def off(): GPIO.output(7,False)

s = 0.1 #Set in conjuction with ReadBlink entry_time
charToBinaryDict = { "A":"101110",
              "B":"1110101010",
              "C":"111010111010",
              "D":"11101010",
              "E":"10",
              "F":"1010111010",
              "G":"1110111010",
              "H":"10101010",
              "I":"1010",
              "J":"10111011101110",
              "K":"1110101110",
              "L":"1011101010",
              "M":"11101110",
              "N":"111010",
              "O":"111011101110",
              "P":"101110111010",
              "Q":"11101110101110",
              "R":"10111010",
              "S":"101010",
              "T":"1110",
              "U":"10101110",
              "V":"1010101110",
              "W":"1011101110",
              "X":"111010101110",
              "Y":"11101011101110",
              "Z":"111011101010",
              "1":"101110111011101110",
              "2":"1010111011101110",
              "3":"10101011101110",
              "4":"101010101110",
              "5":"1010101010",
              "6":"111010101010",
              "7":"11101110101010",
              "8":"1110111011101010",
              "9":"111011101110111010",
              "0":"11101110111011101110",
              " ":"000000"}
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
def sendMessage():
    message = "11111000001111100000"
    origin = input("Origin: ")
    destination = input("Destination: ")
    function = input("Function: ")
    trans = input("Message: ")
    length = str(len(trans))
    text = origin + destination + function + length + trans
    message = message + ''.join([charToBinaryDict[x] for x in text]) + "111111111"
    print(message)
    transmit(message)
    off()
    
print("Transmitter online...")
