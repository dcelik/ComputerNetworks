import queue as q
import RPi.GPIO as GPIO
from receive import receiveMessage
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

messageList = q.Queue();

def popMessage():
	if not messageList.empty():
		return messageList.get();
	else:
		return None;
def monitor():
	while True:
        	messageList.put(receiveMessage())
