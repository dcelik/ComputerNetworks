"""
Chat_Server.py
--------------
Author: Nick Francisci
Purpose: A chat server which allows users to "log in" under an alias and
	then send messages to all other logged on users.
Status: Untested with new modularization
"""

#Future Ideas:
# - Log off users after a period of inactivity
# - Retrict send frequency to restrict spamming and bruteforcing
# - Take 2nd argument from user

import CustomSocket as cs
import GlobalVars as g
import UserCommands as uc
import ServerFunctions as s

class Chat_Server(object):
	
	#------------Run Server------------#
	def __init__(self,IP=g.server_ip,port=g.server_port):
											#	reference class 	address family		UDP/TCP protocol	set time until it returns
		socket, AF_INET, SOCK_DGRAM, timeout = cs.socket, cs.AF_INET, cs.SOCK_DGRAM, cs.timeout
		
		with socket(AF_INET, SOCK_DGRAM) as sock:
			sock.bind((IP,port))
			sock.settimeout(-1) # No timeout
			print ("Chat Server started on IP Address {}, port {}".format(IP,port))
			while True:
				#Check to see if a message is received within timeout
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
						uc.parseCommandString(message[1:],source_IP);
					else:
						#If the user is not logged in, force them to log in
						if g.Users.get(source_IP) is None:
							s.requestConnect(source_IP);
						else:
							s.relayMessage(message, source_IP);

				#If no message is received within timeout, execute this code
				except timeout:
					continue;
				#except KeyboardInterrupt:
				#	sock.close()
				#	print("Socket Closed");
				#	exit(0)
				#except:
				#	#Raise error and proceed
				#	continue;
					
##	def closeSocket(self, sock):
##		""" Ensures that socket is closed on program exit """
##		print(sock)
##		sock.close()

#------------Executing Code------------#
if __name__  == "__main__":
	Chat_Server();