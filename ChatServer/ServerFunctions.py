""" Server Initiated Functions """
import GlobalVars as g
import CN_Sockets

def sendMessage(message, dest_IP):
    """ Sends a message to the destination IP """
    Server_Address=(dest_IP,g.default_client_port)
    socket, AF_INET, SOCK_DGRAM = CN_Sockets.socket, CN_Sockets.AF_INET, CN_Sockets.SOCK_DGRAM
    with socket(AF_INET,SOCK_DGRAM) as sock:
        #Check if string is actually a list and parse if so
        if isinstance(message,list):
            str_message = ''.join(message);
        else:
            str_message = message;

        #Display and log on server
        g.ServerLog.append(str_message);
        print(str_message)
        
        bytearray_message = bytearray(str_message,encoding="UTF-8")
        bytes_sent = sock.sendto(bytearray_message, Server_Address)


def serverWelcome(dest_IP):
        sendMessage("Welcome. You are logged in as " + g.Users[dest_IP].alias + ". Enter " +
                    "\\help to see available commands.", dest_IP);

def requestConnect(dest_IP):
        """ Sends a message to the destination IP requesting a login """
        message = "Please enter a name for yourself by responding in the format: \\connect name"
        sendMessage(message, dest_IP)

def relayMessage(message, source_IP):
        """ Relays a message to all users """
        if len(message)>=g.client_buffer_size-2-len(g.Users[source_IP].alias):
                sendMessage("Message was too long. It has not been sent.", source_IP);
        else:
                for client in [k for k,v in g.Users.items()]:
                        sendMessage(g.Users[source_IP].alias + ": " + message, client);
