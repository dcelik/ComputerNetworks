from catch import *
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

def main():
    x = 0
    print("Receiver Online...")
    z = takeMeasurement()
    initialPacket = [z,1]
    while x == 0:
        # Catch whitespace before message
        currentPacket = catchPacket(initialPacket)
        initialPacket = [not currentPacket[0],2]

        # Catch start sequence
        startSequence = catchPacket(initialPacket)
        initialPacket = [not startSequence[0],2]
        currentPacket = catchPacket(initialPacket)
        initialPacket = [not currentPacket[0],2]

        #Nick's Code is added here - not yet tested:
        pulse_width = startSequence[1]/8
        if startSequence[0]:
        	print("Start sequence received. Listening...")
            catchHeader(initialPacket,pulse_width)
            catchMessage(initialPacket,pulse_width)
        else:
            print("Error. Start sequence not received.")
            print(currentPacket)
            
        initialPacket = [False,2]
if __name__ == "__main__":
    main()


