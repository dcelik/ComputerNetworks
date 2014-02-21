
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
import GlobalVars as g

class Chat_Server(object):
	#------------User Accessible Commands/Command Parsing------------#
	def parseCommandString(self, message, source_IP):
		""" Given a command message, calls the corresponding function and passes any arguments """
		#TODO: Move all user commands to a seperate class
		message = message.split()
		if message is not None:
			command = message[0];
		else: return;
		if len(message)>1:
			argument = message[1];
		else: argument=None;

		#Only allow logged in users to execute commands other than \connect
		if g.Users.get(source_IP) is not None and not command==g.Commands[connect]:
			self.requestConnect(source_IP);
			return;

		#Parse Commands
		if command == g.Commands['set_name']:
			if argument is not None:
				self.setName(argument, source_IP);
			else:
				self.sendMessage("Invalid input. Please enter a valid name in format \\setName [name]",source_IP);
		elif command == g.Commands['connect']:
			if argument is not None:
				self.connect(argument, source_IP);
			else:
				self.sendMessage("Invalid input. Please enter a valid name in format \\connect [name]",source_IP);
		elif command == g.Commands['admin']:
			if argument is not None:
				self.admin(argument, source_IP);
			else:
				self.sendMessage("Invalid password entry. Please enter a valid entry in format \\admin [password]",source_IP);
		elif command == g.Commands['disconnect']:
			self.disconnect(source_IP);
		elif command == g.Commands['disp_users']:
			self.dispUsers(source_IP);
		elif command == g.Commands['get_help']:
			self.sendHelp(source_IP);
		else:
			self.sendMessage("Invalid command.", source_IP);
			
	
	def admin(self, pw, source_IP):
		""" Toggle admin status on user """
		#TODO: add password hashing
		#TODO: add admin commands (print server log, ban IPs, clear server console)
		if pw==g.admin_pw:
			sendMessage(g.Users[source_IP].toggleAdmin(), source_IP);
		else:
			self.sendMessage("Invalid admin login.",source_IP);

	def invisible(self, source_IP):
		""" Toggle invisible status on user """
		#TODO: make invisibility actually have an effect
		sendMessage(g.Users[source_IP].toggleInvisible(),source_IP);

			
	def connect(self, name, source_IP):
		""" Creates a new user session """
		if Users.get(source_IP) is not None:
			self.renewConnection(source_IP);
		elif not name in g.ClientAliases:
			g.Users[source_IP] = User(name);
			g.ClientAliases.append(name);
			self.serverWelcome(source_IP);
		else:
			self.sendMessage("Name already taken.",source_IP);

	def disconnect(self,source_IP):
		""" Delete a user session """
		g.ClientAliases.remove(g.Users(source_IP).alias);
		del g.Users[source_IP];
		self.sendMessage("Successfully logged out.", source_IP);
		
	def setName(self, name, source_IP):
		""" Resets a client's alias """
		if not name in g.ClientAliases:
			g.ClientAliases.remove(g.Users(source_IP).alias);
			g.Users(source_IP).alias = name;
			g.ClientAliases.append(name); 
		else:
			self.sendMessage("Name already taken.", source_IP);

	def dispUsers(self, dest_IP):
		""" Sends a list of all logged in user aliases """
		#TODO: Implement invisibility
		message = "Users currently in chat: \n"
		for user in g.ClientAliases:
			message += user + "\n"
		self.sendMessage(message, dest_IP);
			
	def sendHelp(self, dest_IP):
		""" Sends a message to the destination IP listing (and ideally explaining) functions available to them """
		for command in g.UserCommandList:
			command_string += "//" + command + ", "
		help_message = "Available Commands: " + command_string[:-2];
		self.sendMessage(help_message, dest_IP);
		
	def renewConnection(self,dest_IP):
		""" Not Yet Implemented """
		#TODO: Implement


	#------------Server Functions------------#
	def serverWelcome(self, dest_IP):
		""" Not Yet Implemented """
		#TODO: Implement

	def requestConnect(self, dest_IP):
		""" Sends a message to the destination IP requesting a login """
		message = "Please enter a name for yourself by responding in the format: \\connect name"
		self.sendMessage(message, dest_IP)

	def relayMessage(self, message, source_IP):
		""" Relays a message to all users """
		if len(message)>=g.client_buffer_size:
			self.sendMessage("Message was too long. It has not been sent.", source_IP);
		else:
			for client in [k for k,v in g.Users.items()]:
				self.sendMessage(g.Users[source_IP].alias + ": " + message, client);

	def sendMessage(self, message, dest_IP):
		""" Sends a message to the destination IP """
		Server_Address=(dest_IP,g.default_client_port)
		socket, AF_INET, SOCK_DGRAM = CN_Sockets.socket, CN_Sockets.AF_INET, CN_Sockets.SOCK_DGRAM
		with socket(AF_INET,SOCK_DGRAM) as sock:
			str_message = message
			bytearray_message = bytearray(str_message,encoding="UTF-8")
			bytes_sent = sock.sendto(bytearray_message, Server_Address)


	#------------Run Server------------#
	def __init__(self,IP=g.server_ip,port=g.server_port):
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
					g.ServerLog.append(message);
					print(message);
					
					#Logic for evaluating user commands and relaying messages
					if message[0] == g.command_symbol:
						self.parseCommandString(message[1:],source_IP);
					else:
						#If the user is not logged in, force them to log in
						if g.Users.get(source_IP) is None:
							self.requestConnect(source_IP);
						else:
							self.relayMessage(message, source_IP);

				#If no message is recieved within timeout, execute this code
				except timeout:
					continue

#------------Executing Code------------#
if __name__  == "__main__":
	Chat_Server();
