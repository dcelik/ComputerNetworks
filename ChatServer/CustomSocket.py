import sys
import os
import thread
sys.path.insert(0,os.join(os.getcwd(), os.pardir())); # Add MAC_Identifier location to path
import MAC_Identifier as MAC

class CustomSocket:
	def __init__(self,family,type,router_mac="T",verbose=False):
		""" Initialize a CustomSocket instance """
		# Associate variables with names so they can be retrived by server
		self.AF_INET = 2;
		self.SOCK_DGRAM = 2;
		self.timeout = -1;		

		# Setup booleans to validate that socket is used correctly
		self.validFamilyAndProtocol = False;
		self.validIPAndPort = False;

		# Setup MAC Data
		self.macDict = dict();
		self.macDict['router_mac']  = router_mac;
		self.my_mac = MAC.my_ad;

		self.verbose = verbose;
		pass;

	def socket(self, family, protocol):
		""" Set up a socket with the given arguments. """

		if family!=2:	#AF_INET
			print("Family not valid!");
		else:
			self.family = 2;

		if protocol!=2:	#UDP
			print("Sorry, this sending protocol is not currently supported!");
		else:
			self.protocol = 2;

		#Our "UDP" imports (importing our Morse implementation of UDP)
		if protocol==2: 
			self.validFamilyAndProtocol = True;
			self.protocol_identifier = 'E'; #The standard defined base 36 char designating UDP
			#Setup a path to the morsecode send recieve functions
			path = os.join(os.getcwd(), os.pardir(), "TransmissionModule");
			sys.path.insert(0,path);

			# Import sending related functions
			import transmit as t;

			#  Import recieving related functions
			import monitor as r;


	def bind(self, address):
		""" Start a socket listening for messages addressed to the parent class. """

		# Returns with error if inputs are invalid
		if not self.validFamilyAndProtocol:
			print("Error: Invalid family and protocol or family and protocol are not initialized: socket not bound!");
			return;

		self.my_ip_addr = address[0];
		self.my_port = address[1];
		self.validIPAndPort = True;

		#Starts a monitor function on a new thread that queues messages as they are recieved
		self.queueingThread = thread.start_new_thread(r.monitor(),()); #This may cause a memory leak - unsure.
		
		if self.verbose:
			print("Socket bound. Your IP is " + self.my_ip_addr + ". Your port is " + self.my_port);

	def settimeout(self, timeout):
		""" Sets a message timeout: the timeout is currently unused """
		self.timeout = timeout;

	def sendto(self,msg,address):
		""" Assembles a message and sends it with the down-stack implementation. """

		if not self.validIPAndPort:
			print("Error: Invalid IP and port or socket has not been bound with an IP and port: message not sent!");
			return;

		

		to_ip_addr = address[0];
		to_port = address[1];
		msg = msg.decode("utf-8"); #Convert from bytearray to a string for ease of operation

		# Assemble UDP package
		udp_package = to_port + self.my_port + msg;

		# Assemble IP package
		ip_header = to_ip_addr + self.my_ip_addr + self.protocol_identifier + t.base36encode(len(udp_package)); # Does the base36 encode auto encode to 2 characters? If not, this needs to be done here.
		ip_package = ip_header + udp_package;

		# Assemble MAC package
			# First check to see if the MAC of the recieving IP is known, if not address message to router
		if macDict[to_ip_addr] is not None: mac_to = macDict[to_ip_addr];
		else: mac_to = macDict['router_mac'];	# This only works if you're not the router...
			# Then assemble the remainder of the MAC package
		mac_from = my_mac;
		mac_length = t.base36encode(len(ip_package));	# Does the base36 encode auto encode to 2 characters? If not, this needs to be done here.
		mac_header = mac_to + mac_from + mac_length;
		mac_package = mac_header + ip_package;

		# Send the message
		t.sendMessage(mac_package);

	def baseRecv(self, buflen):
		""" 
		Checks the threaded monitoring function to see if any messages have been recorded. 
		Then it checks to see if the message is addressed to this MAC, IP, and port and returns
		if it is. In the process it records the MAC address of the sending computer into a dict
		for future use. Returns the message with all recorded header data for further processing.

		"""

		# Attempts to retrieve a message from the queue initilized in bind, returns None if there are no messages
		data = r.popMessage();	

		# Checks to see if a message was retrieved
		if data is None:
			return None; # Not certain if this is the correct return for this...
		else:
			message = data[0];	# should header = data[0]?
			header = data[1];	# should message = data[1]?

		mac_header = header[:4]; #Is this true? MAC: 1 char to, 1 char from, 2 char base36 len
		header = header[4:];
		mac_to = mac_header[0];

		ip_header = header[:7];
		header = header[7:];

		udp_header = header;

		# If the message is not addressed to this computer's MAC, discard the message
		if mac_to != self.my_mac: return None;

		

		if (buflen<len(message)): return None;
		else: return message, mac_header, ip_header, udp_header;

	def recvfrom(self, buflen):
		""" The recieve function to be used by standard applications. """

		data = baseRecv(buflen);
		if data is not None:
			message = data[0];
			mac_header = data[1];
			ip_header = data[2];
			udp_header = data[3];

			udp_to = udp_header[0];
			mac_from = mac_header[1];
			ip_from = ip_header[1];
			udp_from = udp_header[1];


			# Add the MAC to the MAC dictionary if it is not already recorded.
			if macDict[ip_from] is None: macDict[ip_from] = mac_from;

			# If the message is not addressed to this computer's IP, discard the message (should be redudant with MAC)
			if ip_to != self.my_ip_addr: return None;

			# If the message is not addressed to this application's port, discard the message
			if udp_to != self.my_port: return None;

			return message, (ip_from,udp_from); 
		else: return None;

	def routerRecvFrom(self, buflen):
		""" 
		Uses the same code as the recieve function, but returns additional data for use
		by the router.

		"""

		data = baseRecv(buflen);
		if data is not None:
			message = data[0];
			mac_header = data[1];
			ip_header = data[2];
			udp_header = data[3];

			ip_to = ip_header[0];
			ip_from = ip_header[1];
			udp_to = udp_header[0];
			udp_from = udp_header[1];

			return message, (ip_from,udp_from) ,(ip_to,udp_to); 
		else: return None;