import queue as q
from receive import receiveMessage
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

messageList = q.Queue();

def popMessage():
	if not messageList.Empty():
		return messageList.get();
	else:
		return None;

while True:
        messageList.put(receiveMessage())
