from CustomSockets import CustomSocket

class RouterSockets(CustomSocket):
  	def __init__(self,Router_Address):
    # initialize the super class
    # figure our the macDict problem
  
  	def sendto(self,msg,address):
  		""" Router Should "forward" a message on, meaning it should not add it's
    	own ip/udp address to the header
    	"""
    	pass
  
  	def recvfrom(self, buflen):
    	# copy code from routerRecvFrom (below)
    	pass
  
  
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
            
  