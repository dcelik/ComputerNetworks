from catch import *

def main():
    x = 0
    print("Receiver Online...")
    #z = takeMeasurement()
    initialPacket = [False,1]
    while x == 0:
        # Catch whitespace before message
        currentPacket = catchPacket(initialPacket)
        initialPacket = [not currentPacket[0],2]
        print(currentPacket)

        # Catch start sequence
        startSequence = catchPacket(initialPacket)
        initialPacket = [not startSequence[0],2]
        print(currentPacket)
        currentPacket = catchPacket(initialPacket)
        initialPacket = [not currentPacket[0],2]
        print(currentPacket)
        
        if startSequence[0] and 35 <= startSequence[1] <= 45:
            print("Start sequence received. Listening...")
            catchHeader(initialPacket)
            catchMessage(initialPacket)
        else:
            print("Error. Start sequence not received.")
            print(currentPacket)

if __name__ == "__main__":
    main()


