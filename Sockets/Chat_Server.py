
"""
Chat_Server.py
--------------
Author: Nick Francisci
Purpose: A chat server which allows users to "log in" under an alias and
	then send messages to all other logged on users.
Status: Command features added 2-19-14, Currently Untested
"""


#Future Ideas:
# - Record dict of usernames that map to IPs and assign that name by default on connect
# - Change implementation of alias - IP to a dict (which it should be)
# - Log off users after a period of inactivity

import CN_Sockets

class Chat_Server(object):
	
	#------------Global Variables------------#
	
	#User keywords to call commands
	command_symbol = "\\";
	set_name_cmd = "setName";
	disp_users_cmd = "users"
	help_cmd = "help"
	connect_cmd = "connect"
	disconnect_cmd = "disconnect"

	#Server Lists
	ConnectedClients = [];
	ClientAliases = [];
	ServerLog = [];

	default_client_port = 5280;


	#------------User Accessible Commands/Command Parsing------------#
	def parseCommandString(self, message, source_IP):
		""" Given a command message, calls the corresponding function and passes any arguments """
		message = message.split()
		command = message[0]
		argument = message[1]

		#Connect user command the correct function
		if command==self.set_name_cmd:
			self.setName(argument, source_IP);
		elif command==self.connect_cmd:
			if source_IP in self.ConnectedClients:
				self.renewConnection()
			elif argument is not None:
				self.setName(argument, source_IP);
			else:
				self.requestName(source_IP);
		elif command==self.disconnect_cmd:
			self.disconnectUser(source_IP)
		elif command==self.help_cmd:
			self.sendHelp(source_IP);
		elif command==disp_users_cmd:
			self.dispUsers(source_IP);
		else:
			self.sendMessage("Invalid command.", source_IP);

	def setName(self, name, source_IP):
		""" Resets a client's alias, or logs them in if they are not already """
		if not name in self.ClientAliases:
			#If client is already logged in, change his or her alias
			if source_IP in self.ConnectedClients: 
				self.ClientAliases[self.ConnectedClients.index(source_IP)] = name;
				
			#If client is not logged in, log in with IP & Alias
			else:   
				self.ConnectedClients.append(source_IP);
				self.ClientAliases(name);

		#Do not allow multiple users to use the same alias at once   
		else:
			self.sendMessage("Name already taken.", source_IP);

	def dispUsers(self, dest_IP):
		""" Sends a list of all logged in users' aliases to the destination IP """
		message = "Users currently in chat: \n"
		for user in self.ClientAliases:
			message += user + "\n"
		self.sendMessage(message, dest_IP);
			
	def disconnectUser(self,source_IP):
		""" Removes a user from the chat server by removing their IP and Alias from their respective lists """
		ind = self.ConnectedClients.index(source_IP);
		self.ConnectedClients.pop(ind);
		self.ClientAliases.pop(ind);

	def sendHelp(self, dest_IP):
		""" Sends a message to the destination IP listing (and ideally explaining) functions available to them """
		help_message = "Available Commands: \\connect (name), \\setName name, \\disconnect, \\users, \\help";
		self.sendMessage(help_message, dest_IP);
		
	def renewConnection(self,dest_IP):
		""" Not Yet Implemented """


	#------------Server Functions------------#
	def serverWelcome(self, dest_IP):
		""" Not Yet Implemented """

	def requestName(self, dest_IP):
		""" Sends a message to the destination IP requesting a login """
		message = "Please enter a name for yourself by responding in the format: \\setName name"
		sendMessage(message, dest_IP)

	def relayMessage(self, message, source_IP):
		""" Relays a message to all connected clients """
	
		#Attach sender alias to message
		message = self.ClientAliases(self.ConnectedClients.index(source_IP)) + ": " + message;

		for client in self.ConnectedClients:
			self.sendMessage(message, client);

	def sendMessage(self, message, dest_IP):
		""" Sends a message to the destination IP """
		Server_Address=(dest_IP,self.default_client_port)
		socket, AF_INET, SOCK_DGRAM = CN_Sockets.socket, CN_Sockets.AF_INET, CN_Sockets.SOCK_DGRAM
		with socket(AF_INET,SOCK_DGRAM) as sock:
			str_message = message
			bytearray_message = bytearray(str_message,encoding="UTF-8")
			bytes_sent = sock.sendto(bytearray_message, Server_Address)


	#------------Run Server------------#
	def __init__(self,IP="127.0.0.1",port=5280):
		socket, AF_INET, SOCK_DGRAM, timeout = CN_Sockets.socket, CN_Sockets.AF_INET, CN_Sockets.SOCK_DGRAM, CN_Sockets.timeout
		with socket(AF_INET, SOCK_DGRAM) as sock:
			sock.bind((IP,port))
			sock.settimeout(2.0) # 2 second timeout
			print ("Chat Server started on IP Address {}, port {}".format(IP,port))
			while True:
				#Check to see if a message is recieved within timeout
				try:
					bytearray_msg, address = sock.recvfrom(65536)
					source_IP, source_port = address

					#Actual message handling
					print ("\nMessage received from ip address {}, port {}:".format(source_IP,source_port))
					message = bytearray_msg.decode("UTF-8");
					self.ServerLog.append(message);
					print(message);

					#Logic for evaluating user commands and relaying messages
					if message[0] == self.command_symbol:
						self.parseCommandString(message[1:],source_IP);
					else:
						#If the user is not logged in, force them to log in
						if not source_IP in self.ConnectedClients:
							self.requestName(source_IP);
						else:
							self.relayMessage(message, source_IP);

				#If no message is recieved within timeout, execute this code
				except timeout:
					#print (".",end="",flush=True)
					continue

#------------Executing Code------------#
if __name__  == "__main__":
	Chat_Server();
