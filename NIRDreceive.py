from getPulseWidth import getPulseWidth
from monitor import *
from chunk import *
from translator import *

def main():
    print("Receiver Online...")
    while True:
        print("Listening for transmissions...")
        start_of_msg = MonitorStartOfMsg()
        print("Receiving transmission...")
        binary = start_of_msg + CaptureMessage()
        print("Transmission Received!")
        pwidth = getPulseWidth(binary,True)
        print("Pulse width = " + str(pwidth))
        consolidated = consolidate(binary, pwidth)
        print(consolidated)
        print(trans2Mess(''.join([fromBoolean(d) for d in consolidated])))
        

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


