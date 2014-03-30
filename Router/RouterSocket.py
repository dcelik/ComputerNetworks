from CustomSockets import CustomSocket

class RouterSockets(CustomSocket):
  	def __init__(self,Router_Address):
    # initialize the super class
    # figure our the macDict problem
  
  	def sendto(self,msg,address):
  		""" Router Should "forward" a message on, meaning it should not add it's
    	own ip/udp address to the header
    	"""
    	address = self.pubIPToMorse(address);
        
        if not self.validIPAndPort:
            print("Error: Invalid IP and port or socket has not been bound with an IP and port: message not sent!");
            return;

        to_ip_addr = address[0];
        to_port = address[1];
        msg = msg.decode("utf-8"); #Convert from bytearray to a string for ease of operation

        # Assemble UDP package
        udp_package = to_port + self.my_port + msg;

        # Assemble IP package
        ip_header = to_ip_addr + self.my_ip_addr + self.protocol_identifier + t.base36encode(len(udp_package));
        ip_package = ip_header + udp_package;

        # Assemble MAC package
            # First check to see if the MAC of the recieving IP is known, if not address message to router
        if to_ip_addr in self.macDict: mac_to = self.macDict[to_ip_addr];
        else: mac_to = self.macDict['router_mac'];   # This only works if you're not the router...
            # Then assemble the remainder of the MAC package
        mac_from = self.my_mac;
        # Send the message
        t.sendMessage(mac_to,mac_from,ip_package);
  
  	def recvfrom(self, buflen):
    	# copy code from routerRecvFrom (below)
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

			bytearray_msg = bytearray(message, encoding="utf-8")

			return bytearray_msg, (ip_from,udp_from) , (ip_to,udp_to), ip_header, udp_header; 
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
            
  