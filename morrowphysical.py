import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime
from queue import Queue
from morrowglobals import charToBinaryDict,binaryToCharDict

#------------------SETUP------------------#

output_pin = 7
input_pin = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(output_pin,GPIO.OUT)
GPIO.setup(input_pin,GPIO.IN)
GPIO.setwarnings(False)
#------------------CLASS------------------#
class MorrowNIC(object):
	def __init__(self):
		self.pulse_duration = .01*1000000
		self.pulse_width = None

		self.previous_edge = datetime.now()
		self.current_edge = None

		self.last_pulse = None
		
		self.transmission_queue = Queue()
		self.pulse_queue = Queue()
		
		self.bus_state = GPIO.input(input_pin)
		self.receiving_state = False

		GPIO.add_event_detect(input_pin,GPIO.BOTH,callback=self.edgeFound)

	def edgeFound(self,pin):
		self.current_edge = datetime.now()
		delta = self.current_edge-self.previous_edge
		pulse = (self.bus_state,delta.seconds*1000000 + delta.microseconds)
		self.previous_edge = self.current_edge
		self.bus_state = GPIO.input(input_pin)

		if pulse[0] and pulse[1] >= 3.5*self.pulse_duration:
			if not self.receiving_state:
				self.pulse_width = pulse[1]/4.0
			if self.receiving_state:
				self.pushTransmission()
			self.receiving_state = not self.receiving_state
			return
		
		if self.receiving_state:
			self.pulse_queue.put(pulse)
			
	def pushTransmission(self):
		transmission = ""
		whitespace = self.pulse_queue.get()
		assert whitespace[0] == 0
		while not self.pulse_queue.empty():
			pulse = self.pulse_queue.get()
			length = pulse[1]
			if pulse[1] >= self.pulse_width*0.5 and pulse[1] <= self.pulse_width*2.0:
				length = 1
			elif pulse[1] > self.pulse_width*2.0 and pulse[1] <= self.pulse_width*4.0:
				length = 3
			elif pulse[1] > self.pulse_width*6.0 and pulse[1] <= self.pulse_width*8.0:
				length = 7
			else:
				length = 0
			transmission += str(pulse[0])*int(length)
		transmission = self.errorCorrect(transmission)
		self.transmission_queue.put(transmission)

	def errorCorrect(self,transmission):
		return transmission

	def convertToText(self,transmission):
		sections = []
		words = transmission.split("0000000")
		for word in words:
			characters = word.split("000")
			chars = [char + "000" for char in characters]
			sections.extend(chars)
			sections.append("0000")
		while '000' in sections:
			sections.remove('000')
		if sections[-1] == "0000":
			sections = sections[:-1]
		print(sections)
		text = ''.join([binaryToCharDict[binary] for binary in sections])
		return text

	def convertToTransmission(self,text):
		while text[0] == " ":
			text = text[1:]
		text = text.upper()
		marker_code = "11110"
		binary = ''.join([charToBinaryDict[char] for char in text])
		print(binary)
		return marker_code + binary + marker_code
	
	def transmit(self,trans):
		GPIO.setup(output_pin,GPIO.OUT)
		for i in range(len(trans)):
			if trans[i] == '1':
				GPIO.output(output_pin,GPIO.HIGH)
				sleep(self.pulse_duration/1000000)
			else:
				GPIO.output(output_pin,GPIO.LOW)
				sleep(self.pulse_duration/1000000)
		GPIO.output(output_pin,GPIO.LOW)
		GPIO.setup(output_pin,GPIO.IN)
		
			

if __name__ == "__main__":
	s = .01
	GPIO.output(7,GPIO.LOW)
	nic = MorrowNIC()
	sleep(1)
	nic.transmit(nic.convertToTransmission(" Hello Nick"))
	sleep(1)
	trans = nic.transmission_queue.get()

	print(len(trans))
	print(nic.convertToText(trans))
