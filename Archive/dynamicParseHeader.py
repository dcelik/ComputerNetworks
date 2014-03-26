"""
dynamicParseHeader(pw)
INPUTS: integer pulse width of the transmission represented by the variable "pw"
OUTPUTS: list of 3 characters, 1 integer, and the last bit of the transmission to be passed on to dynamicParseMessage
         [origin, destination, function, length in characters, end of transmission] for example ["A","D","E",1234,[True,True,True]]
"""
import RPi.GPIO as GPIO
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

def dynamicParseHeader(pw):
    shouldSee = True
    binaryCache = []
    morseCache = []
    header = []
    while len(header) < 7:
        lookingBinary = True
        differenceAlreadyFound = False
        while lookingBinary == True:
            time.sleep(pause)
            status = takeMeasurement()
            #status = takeKeyboardInput()
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
        if len(morseCache) > 4:
            if morseCache[-4:] == [False,False,False,True]:
                print("End of Character")
                binaryString = ''.join([str(int(n)) for n in morseCache[:-3]])
                header.append(binaryToCharDict[binaryString])
                print(header)
                morseCache = [True]
            elif morseCache[-6:] == [False,False,False,True,True,True]:
                print("End of Character")
                binaryString = ''.join([str(int(n)) for n in morseCache[:-5]])
                header.append(binaryToCharDict[binaryString])
                print(header)
                morseCache = [True,True,True]
            #elif morseCache[-4:] == [False,False,False,False,False,False,False,True]:
                #print("End of Word")
                #lookingMorse = False
    finalheader = [header[0],header[1],header[2],(int(header[3])*1000 + int(header[4])*100 + int(header[5])*10 + int(header[6])), morseCache]
    return finalheader
                
        
