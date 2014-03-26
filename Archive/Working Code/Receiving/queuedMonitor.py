import queue as q
from catch import *
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

messageList = q.Queue();

def popMessage():
	if not messageList.Empty():
		return messageList.get();
	else:
		return None;

def monitor(verbose=False):
    x = 0
    if verbose: print("Receiver Online...");
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

        pulse_width = startSequence[1]/4

        if startSequence[0]:
        	#Listen to message and push it to the queue as a (header,message) tuple
        	if verbose: print("Start sequence received. Listening...");
            messageList.put((catchHeader(initialPacket,pulse_width),catchMessage(initialPacket,pulse_width));
        else:
        	if verbose:
           		print("Error. Start sequence not received.");
            	print(currentPacket);
            
        initialPacket = [False,2];