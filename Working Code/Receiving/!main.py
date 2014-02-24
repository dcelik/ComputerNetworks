from catchPacket import *

def main():
    print("Receiver Online...")
    z = takeMeasurement()
    initialPacket = [z,1]
    while True:
        currentPacket = catchPacket(initialPacket)
        initialPacket = [not currentPacket[0],2]
        print(currentPacket),

if __name__ == "__main__":
    main()


