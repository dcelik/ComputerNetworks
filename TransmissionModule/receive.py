from catch import *
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

def receiveMessage():
        x = 0
        print("Receiver Online...")
        z = takeMeasurement()
        initialPacket = [z,1]
        # Catch whitespace before message
        currentPacket = catchPacket(initialPacket)
        initialPacket = [not currentPacket[0],2]

        # Catch start sequence
        startSequence = catchPacket(initialPacket)
        initialPacket = [not startSequence[0],2]
        currentPacket = catchPacket(initialPacket)
        initialPacket = [not currentPacket[0],2]

        #Actually get the message
        pulse_width = startSequence[1]/4
        #print(pulse_width)
        if startSequence[0]:
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
        length = header[3:]
        print("Group code: " + group_code)
        print("Header: " + header[0:3] + " " + str(base36decode(length)))
        print("Message received:")
        print(message[1:-1])
        initialPacket = [False,2]
        return [group_code, header, message[:-1]]

