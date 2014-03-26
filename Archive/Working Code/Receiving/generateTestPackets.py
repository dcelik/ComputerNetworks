message = "111101010001110100010111010001011100011101110111011101110001011101000111000101010100010100010101000000010100010101000000010111000000010111010100011101110111000111010001110111010000000111000100010101000111000000011101110001000101010001010100010111000111011101000100010111010111010"
testPackets = []
for n in range(147):
    #print(message)
    if message[:7] == "0000000":
        testPackets.append([False,70])
        message = message[7:]
    elif message[:3] == "000":
        testPackets.append([False,30])
        message = message[3:]
    elif message[0] == "0":
        testPackets.append([False,10])
        message = message[1:]
    elif message[:4] == "1111":
        testPackets.append([True,40])
        message = message[4:]
    elif message[:3] == "111":
        testPackets.append([True,30])
        message = message[3:]
    elif message[0] == "1":
        testPackets.append([True,10])
        message = message[1:]
print(testPackets)
