import CN_Sockets

class Chat_Server(object):


	ConnectedClients = []
	default_client_port = 5280;
	
	def relayMessage(self, message, source_IP):
		message = str(source_IP) + ": " + message;

		for client in self.ConnectedClients:
			self.sendMessage(message, client);
		


	def sendMessage(self, message, dest_IP):
		Server_Address=(dest_IP,self.default_client_port)

		socket, AF_INET, SOCK_DGRAM = CN_Sockets.socket, CN_Sockets.AF_INET, CN_Sockets.SOCK_DGRAM

		with socket(AF_INET,SOCK_DGRAM) as sock:
			str_message = message
				
			bytearray_message = bytearray(str_message,encoding="UTF-8")

			bytes_sent = sock.sendto(bytearray_message, Server_Address)


	
	def __init__(self,IP="10.7.24.218",port=5280):

		

		socket, AF_INET, SOCK_DGRAM, timeout = CN_Sockets.socket, CN_Sockets.AF_INET, CN_Sockets.SOCK_DGRAM, CN_Sockets.timeout
		
		with socket(AF_INET, SOCK_DGRAM) as sock:
			sock.bind((IP,port))
			sock.settimeout(2.0) # 2 second timeout
			
			print ("Chat Server started on IP Address {}, port {}".format(IP,port))
			
			while True:
				try:
					bytearray_msg, address = sock.recvfrom(65536)
					source_IP, source_port = address

					
					
					print ("\nMessage received from ip address {}, port {}:".format(
					source_IP,source_port))

					message = bytearray_msg.decode("UTF-8");
					print (message)
					if not source_IP in self.ConnectedClients:
						self.ConnectedClients.append(source_IP);
					self.relayMessage(message, source_IP);
			

				except timeout:
					#print (".",end="",flush=True)
					continue

	
if __name__  == "__main__":
        Chat_Server();
