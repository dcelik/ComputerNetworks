class CustomSocket:
	def __init__(self,family,type):
		self.AF_INET = 2;
		self.SOCK_DGRAM = 2;
		self.timeout = -1;

		pass;

	def socket(self, family, protocol):
		if family!=2:
			print("Family not valid!");
		else:
			self.family = 2;

		if protocol!=2:
			print("Protocol not valid!");
		else:
			self.protocol = 2;

		if protocol==2:
			import !main as m #needs to be directed to correct path (within receive)
			import transmit as t # needs to be directe to correct path


	def bind(self, address):
		self.my_ip_addr = address[0];
		self.my_port = address[1];

	def sendto(address,msg):
		self.to_ip_addr = address[0];
		self.to_port = address[1];
		self.msg = msg;



	def recvfrom(buflen):
		message = m.message();

		if (buflen>len(message)):
			return message,(self.from_ip_addr,self.from_port);  

		return "Message has exceeded buffer length!",(self.from_ip_addr,self.from_port);