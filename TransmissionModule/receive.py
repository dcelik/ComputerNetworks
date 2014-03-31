import sys
import os
from catch import *
from transmit import transmit
import translator as translator
from variables import blink_time
from utilities import calc_checksum
sys.path.insert(0,os.path.join(os.getcwd(), os.pardir)); # Add MAC_Identifier location to path
import MAC_Identifier as MAC
sys.path.insert(0,os.path.join(os.getcwd(), os.pardir, "TransmissionModule"));

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
myMAC = MAC.my_ad

def receiveMessage():
        """

        returns: [destinationMAC, sourceMAC,length, ipheader_udpheader_msg]

        where ipheader_udpheader_msg = ipheader + udpheader + msg
        """

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
                #print(pulse_width)
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
                length = base36decode(header[2:4])
                checksum = header[4:]
                if len(message[1:-1]) == length and checksum == calc_checksum(header[0:4] + message[1:-1]):
                        if destinationMAC == myMAC:
                                sendAck(destinationMAC)
                                print("Message received. Ack sent.")
                        ipheader_udpheader_msg = message[:-1] # Clarification of what "message" means throughout the stack
                        print("Header: " + destinationMAC + " " + sourceMAC + " " + str(length) + " " + header[4:])
                        print("Payload received:")
                        print(message[1:-1])
                        print("Calculated length: " + str(len(message[1:-1])))
                        print("Calculated checksum: " + calc_checksum(header[0:4] + message[1:-1]))
                        time.sleep(0.8) 
                        return [destinationMAC,sourceMAC,length, ipheader_udpheader_msg]
        return False #if in three trials, the message could not be received, return False.



def sendAck(destination):
        ack = header_pulse + translator.mess2Trans(destination ) + '1';
        print(ack)
        transmit(ack, blink_time)
        print("Ack sent.")
        return True
