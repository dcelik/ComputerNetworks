from getPulseWidth import getPulseWidth
from monitor import *
from chunk import *
from translator import *
from readStartSequence import *
from dynamicParseHeader import *
from dynamicParseMessage import *


pause = .1

def main():
    print("Receiver Online...")
    while True:
        print("Listening for transmissions...")
        start_of_msg = MonitorStartOfMsg()
        print("Receiving transmission...")
        print(start_of_msg)
        pwidth = readStartSequence(start_of_msg)
        print(pwidth)
        header = dynamicParseHeader(pwidth)
        print(header)
        message = dynamicParseMessage(pwidth,header)
        #remaining_binary_message = CaptureMessage()
        print("Transmission Received!")
        print("Pulse width = " + str(pwidth))
        print("Message = " + message)
        #consolidated = consolidate(known_sample_header+remaining_binary_message, pwidth)
        #print(consolidated)
        #print(trans2Mess(''.join([fromBoolean(d) for d in consolidated])))
        

def fromBoolean(d):
    if d:
        return '1'
    else:
        return '0'

def toBool(d):
    if d=='1':
        return True;
    else:
        return False;

if __name__ == "__main__":
    main()


