
import CN_Sockets # CN_Sockets adds ability to interrupt "while True" loop with ctl-C
import CustomSockets    

           
class CN_RouterSender(object):
    """ Computer Networks Chapter 4: Sockets.  UDP Client example. """ 
    
    team = 'I'
    mac = 'R'
    eth_ip = '192.168.100.{}'.format(self.team)
    morse_ip = '0.0.{}.{}'.format(self.team,self.mac)

    def __init__(self,Router_Address=(self.eth_ip,5280)):

        socket, msocket, AF_INET, SOCK_DGRAM = CN_Sockets.socket, CustomSockets.socket, CN_Sockets.AF_INET, CN_Sockets.SOCK_DGRAM

        self.Router_Address = Router_Address

        with socket(AF_INET,SOCK_DGRAM) as sock:
            with msocket(AF_INET,SOCK_DGRAM) as msock:
                
                sock.bind(self.eth_ip,5280)
                sock.settimeout(2.0) # 2 second timeout
                msock.bind(self.morse_ip,5280)  
                msock.settimeout(2.0) # 2 second timeout
                
                print ("UDP_Sender started for CN_RouterSender at IP address {} on port {}".format(
                    Router_Address[0],Router_Address[1])
                       )
                
                while True:
                    try:
                        # Receive Messages from LAN
                        bytearray_msg, source_address, destination_address = msock.routerRecvfrom(1024) # special router recvfrom function
                        source_IP, source_port = source_address
                        destination_IP, destination_port = destination_address

                        print ("\n{} byte message received from ip address {}, port {}:".format(len(bytearray_msg),source_IP,source_port))
                        print ("\n"+bytearray_msg.decode("UTF-8"))

                        # destination_IP example: IA, where I is team, A is mac
                        destination_team, destination_mac = destination_IP

                        if self.team == destination_team:
                            # Route to own team over morse net
                            msock.sendto(bytearray_msg, destination_address)
                            print ("\n{} byte message routed via morsenet")
                        else:
                            # Route to other team's router over ethernet
                            sock.sendto(bytearray_msg, destination_address)
                            print ("\n{} byte message routed via ethernet")

                    except timeout:
                        print (".",end="",flush=True)
                        continue                
                

        print ("UDP_Client ended")

    



               
    
                
                
                
            



            
        
