"""
Chat_Client.py

Olin College Computer Networks Spring 2014
Team NIRD (Nick, Ian, Ryan, Deniz)
"""

from UDP_Server import * 
from UDP_Client import *

class Chat_Client(object):

	def __init__(self):
		self.user_name = input("Provide a user name: ")
		self.server_IP = input("Input the IP of your Chat Room Server: ")
		self.client_IP = CN_Sockets.gethostbyname(CN_Sockets.getfqdn())
		self.port = 5280

		# start own UDP_Server to receive broadcasts from the Chat_Server
		UDP_Server(self.server_IP)
		
		# start own UDP_Client to send messages to the Chat_Server
		UDP_Client((self.client_IP, self.port))
	
if __main__ == "__main__":
	Chat_Client()