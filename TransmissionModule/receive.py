from catch import *
from transmit import sendAck
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
                
                if type(pulse_width) == int:
                        #print("Start sequence received. Listening...")
                        group_code = catchGroupCode(initialPacket,pulse_width)
                        header = catchHeader(initialPacket,pulse_width)
                        message = catchMessage(initialPacket,pulse_width)
                else:
                        print("Error. Start sequence not received.")
                        print(currentPacket)

                origin = header[0]
                destination = header[1]
                function = header[2]
                length = base36decode(header[3:])
        ##        print("Group code: " + group_code)
        ##        print("Header: " + header[0:3] + " " + str(base36decode(length)))
        ##        print("Message received:")
        ##        print(message[1:-1])
                if len(message[:-1]) == length:
                        print("Message received. Sending ack.")
                        sendAck(destination)
                        return [origin,destination,function,length, message[:-1]]
        return False #if in three trials, the message could not be received, return False.

def receiveAck(destination):
        initialPacket = [False,1]
        #Catch whitespace before ack
        currentPacket = catchPacket(initialPacket,True,1)
        initialPacket = [not currentPacket[0],2]
        if currentPacket == None: #If no ack received return False
                return False
        #Catch start sequence and determine pulse width
        pulse_width = catchStartSequence(initialPacket)
        ack = catchAck(pulse_width)
        if ack == destination:
                return True
        else:
                return False

