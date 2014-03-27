
import CN_Sockets # CN_Sockets adds ability to interrupt "while True" loop with ctl-C
import CustomSockets    

           
class CN_RouterSender(object):
    """ Computer Networks Chapter 4: Sockets.  UDP Client example. """ 
    
    team = 'I'
    mac = 'R'
    eth_ip = '192.168.100.{}'.format(self.team)
    morse_ip = '0.0.{}.{}'.format(self.team,self.mac)

    def __init__(self,Router_Address=(eth_ip,5280)):

        socket, msocket, AF_INET, SOCK_DGRAM = CN_Sockets.socket, CustomSockets.socket, CN_Sockets.AF_INET, CN_Sockets.SOCK_DGRAM

        self.Router_Address = Router_Address

        with socket(AF_INET,SOCK_DGRAM) as sock:
            with msocket(AF_INET,SOCK_DGRAM) as msock:

                sock.settimeout(2.0) # 2 second timeout
                msock.bind(self.morse_ip,5280)
                msock.settimeout(2.0) # 2 second timeout
                
                print ("UDP_Client started for CN_RouterSender at IP address {} on port {}".format(
                    Server_Address[0],Server_Address[1])
                       )
                
                while True:
                    try:
                        # Receive Messages from LAN
                        bytearraymsg_to_send, source_address, destination_address = msocket.routerRecvfrom(1024) # special router recvfrom function
                        source_IP, source_port = source_address
                        destination_IP, destination_port = destination_address

                        # destination_IP example: IA, where I is team, A is mac
                        destination_team, destination_mac = destination_IP

                        if self.team == destination_team:
                            # Route to own team over morse net
                            msock.sendto(bytearraymsg_to_send, destination_address) 
                        else:
                            # Route to other team's router over ethernet
                            sock.sendto(bytearraymsg_to_send, destination_address)

                    except timeout:
                        print (".",end="",flush=True)
                        continue                
                

        print ("UDP_Client ended")

    



               
    
                
                
                
            



            
        
