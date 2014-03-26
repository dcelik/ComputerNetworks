from catch import *
from transmit import transmit
import translator as translator
from variables import blink_time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

def receiveMessage():
        trials = 0
        while trials < 3:
                trials += 1
                print("Receiver Online...")
                initialPacket = [False,1]
                #Catch whitespace before message
                currentPacket = catchPacket(initialPacket)
                initialPacket = [not currentPacket[0],2]
                #Catch start sequence and determine pulse width
                pulse_width = catchStartSequence(initialPacket)
                print(pulse_width)
                if pulse_width != None:
                        #print("Start sequence received. Listening...")
                        header = catchHeader(initialPacket,pulse_width)
                        message = catchMessage(initialPacket,pulse_width)
                else:
                        print("Error. Start sequence not received.")
                        print(currentPacket)
                        break

                destinationMAC = header[0]
                sourceMAC = header[1]
                length = base36decode(header[2:])
                print("Header: " + destinationMAC + " " + sourceMAC + " " + str(length))
                print("Payload received:")
                print(message[1:-1])
                if len(message[1:-1]) == length:
                        print("Message received. Sending ack.")
                        sendAck(destinationMAC)
                        return [destinationMAC,sourceMAC,length, message[:-1]]
        return False #if in three trials, the message could not be received, return False.



def sendAck(destination):
        ack = header_pulse + translator.mess2Trans(destination ) + '1';
        print(ack)
        transmit(ack, blink_time)
        print("Ack sent.")
        return True
