
"""
Chat_Server.py
--------------
Author: Nick Francisci
Purpose: A chat server which allows users to "log in" under an alias and
	then send messages to all other logged on users.
Status: Command features added 2-19-14, Tested against Deniz's persistant best efforts to hack it
"""

#Future Ideas:
# - Record dict of usernames that map to IPs and assign that name by default on connect
# - Change implementation of alias - IP to a dict (which it should be)
# - Log off users after a period of inactivity
# - Modularize into classes

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
	admin_cmd = "admin"
	
	#Server Lists
	ConnectedClients = [];
	ClientAliases = [];
	Users = {};
	ServerIPChecks = {};
	ServerLog = [];

	default_client_port = 5280;
	client_buffer_size = 1024;
	message_per_timeout_limit = 5;
	admin_pw = "nick";


	#------------User Accessible Commands/Command Parsing------------#
	def parseCommandString(self, message, source_IP):
		""" Given a command message, calls the corresponding function and passes any arguments """
		message = message.split()
		print(message)
		if message is not None:
			command = message[0];
		else: return;
		if len(message)>1:
			argument = message[1];
		else: argument=None;

		if source_IP not in self.ConnectedClients and not (command==self.set_name_cmd or command==self.connect_cmd):
			self.sendMessage("Please connect with \\connect [name] or \\setName [name]", source_IP);
			return;

		#Connect user command the correct function
		if command==self.set_name_cmd:
			if argument is not None:
				self.setName(argument, source_IP);
		elif command==self.connect_cmd:
			if source_IP in self.ConnectedClients:
				self.renewConnection(source_IP)
			elif argument is not None:
				self.setName(argument, source_IP);
			else:
				self.requestName(source_IP);
		elif command==self.disconnect_cmd:
			self.disconnectUser(source_IP)
		elif command==self.help_cmd:
			self.sendHelp(source_IP);
		elif command==self.disp_users_cmd:
			self.dispUsers(source_IP);
		elif command==self.admin_cmd:
			if argument is not None:
				self.validateAdmin(argument,source_IP);
		else:
			self.sendMessage("Invalid command.", source_IP);

	def validateAdmin(self, pw, source_IP):
		if pw==self.admin_pw:
			self.setName("admin",source_IP,True);
		else:
			self.sendMessage("Invalid admin login",source_IP);
			return;

	def setName(self, name, source_IP, admin_override=False):
		""" Resets a client's alias, or logs them in if they are not already """
		if (name=="admin" or name=="Admin") and admin_override==False:
			self.sendMessage("Invalid Username.",source_IP);
			return;
			
		if not name in self.ClientAliases:
			#If client is already logged in, change his or her alias
			if source_IP in self.ConnectedClients: 
				self.ClientAliases[self.ConnectedClients.index(source_IP)] = name;
			#If client is not logged in, log in with IP & Alias
			else:   
				self.ConnectedClients.append(source_IP);
				self.ClientAliases.append(name);

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
		self.sendMessage(message, dest_IP)

	def relayMessage(self, message, source_IP):
		""" Relays a message to all connected clients """

		if len(message)>=self.client_buffer_size:
			self.sendMessage("Message was too long. It was not sent.", source_IP);
			return;
	
		#Attach sender alias to message
		message = self.ClientAliases[self.ConnectedClients.index(source_IP)] + ": " + message;

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
	def __init__(self,IP="10.7.8.17",port=5280):
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
					
					#Restrict Spamming/Bruteforcing
					#if ServerIPChecks[sourceIP]==0:
					#        ServerIPChecks
					
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
					continue

#------------Executing Code------------#
if __name__  == "__main__":
	Chat_Server();
