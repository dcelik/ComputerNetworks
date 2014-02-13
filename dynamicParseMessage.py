"""
dynamicParseMessage(pw, header)
INPUTS: integer pulse width of the transmission represented by the variable "pw"
        header carried over from the end of the dynamic header parsing
OUTPUTS: message as a string
"""
#import RPi.GPIO as GPIO
import time as time
from chunk import *
from NIRDreceive import pause


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
              "0":"11101110111011101110"}

binaryToCharDict = {v:k for(k,v) in charToBinaryDict.items()}

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

def takeKeyboardInput():
    status = input('Measurement: ')
    if int(status) == 1:
        return True
    else:
        return False

def dynamicParseHeader(pw,header):
    shouldSee = False
    binaryCache = []
    morseCache = header[4]
    while len(message) < header[3]:
        lookingBinary = True
        differenceAlreadyFound = False
        while lookingBinary == True:
            time.sleep(pause)
            #status = takeMeasurement()
            status = takeKeyboardInput()
            binaryCache.append(status)
            if status != shouldSee and differenceAlreadyFound == True:
                print("Evaluation Caused")
                binaryCache = binaryCache[:-2]
                lookingBinary = False
            elif status != shouldSee and differenceAlreadyFound == False:
                differenceAlreadyFound = True
                print("I'm not seeing what I should see")
                print(binaryCache)
            elif status == shouldSee and differenceAlreadyFound == True:
                # fix one bit error
                differenceAlreadyFound = False
                assert binaryCache[-2] != shouldSee
                binaryCache[-2] = shouldSee
                print("One Bit error ignored")
                print(binaryCache)
                print(differenceAlreadyFound)
        print(binaryCache)
        consolidated = consolidate(binaryCache,pw)
        for n in range(len(consolidated)):
            morseCache.append(consolidated[n])
        print(morseCache)
        if shouldSee == True: # now look for the other type of input 
            shouldSee = False
            binaryCache = [False,False]
        else:
            shouldSee = True
            binaryCache = [True,True]
        if len(morseCache) > 5:
            if morseCache[-4:] == [False,False,False,True]:
                print("End of Character")
                binaryString = ''.join([str(int(n)) for n in morseCache[:-3]])
                message.append(binaryToCharDict[binaryString])
                print(message)
                morseCache = [True]
            elif morseCache[-6:] == [False,False,False,True,True,True]:
                print("End of Character")
                binaryString = ''.join([str(int(n)) for n in morseCache[:-5]])
                message.append(binaryToCharDict[binaryString])
                print(message)
                morseCache = [True,True,True]
            elif morseCache[-8:] == [False,False,False,False,False,False,False,True]:
                print("End of Word")
                message.append(' ')
                morseCache = [True]
                print(message)
            elif morseCache[-10:] == [False,False,False,False,False,False,False,True,True,True]:
                print("End of Word")
                message.append(' ')
                morseCache = [True,True,True]
                print(message)
    finalmessage = ''.join(message)     
    return finalmessage
                
        
