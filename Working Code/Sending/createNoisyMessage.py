"""
sendNoisyMessage.py
"""

import random

pulse = 10

morseDict = { "A":".-","B":"-...","C":"-.-.","D":"-..","E":".","F":"..-.",
    "G":"--.","H":"....","I":"..","J":".---","K":"-.-","L":".-..",
    "M":"--","N":"-.","O":"---","P":".--.","Q":"--.-","R":".-.",
    "S":"...","T":"-","U":"..-","V":"...-","W":".--","X":"-..-",
    "Y":"-.--","Z":"--..","1":".----","2":"..---","3":"...--",
    "4":"....-","5":".....","6":"-....","7":"--...","8":"---..",
    "9":"----.","0":"-----"}


transDict = {"-":pulse*3,".":pulse*1,"c":pulse*2,"s":pulse*1,"w":pulse*4}

"""
HELPER FUNCTIONS
"""
def morse2Trans(morse):
    return ''.join([symbol2Trans(symbol) for symbol in morse]) + ''.join('0'*noisyGauss(transDict["c"]))

def mess2Trans(message):
    message = message.upper()
    return ''.join([char2Trans(char) for char in message])

def noisyGauss(n):
	"""
	arg:
		n: integer (number of '1' or '0' to be sent)

	return
		number on a gaussian distribution with mean n

	"""
	return int(random.gauss(n, 1))

def char2Trans(char):
    if char == " ":
        return ''.join('0'*noisyGauss(transDict['w']))

    if morseDict.get(char) is not None:
        return ''.join(morse2Trans(morseDict[char]))
    else:
        return '';

def symbol2Trans(symbol):
    if transDict.get(symbol) is not None:
        return ''.join('1'*noisyGauss(transDict[symbol]))+"".join('0'*noisyGauss(transDict["s"]))
    else:
        return '';

def createNoisyMessage(message):
    """
    Sends a message from the user
    message = the message to be transmitted as a string
    """
    
    return mess2Trans(message);

if __name__ == '__main__':
 	print createNoisyMessage('Hi Ian Hill')