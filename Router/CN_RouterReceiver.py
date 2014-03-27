import CN_Sockets
import CustomSockets

class CN_RouterReceiver(object):
    
    team = 'I'
    mac = 'R'
    eth_ip = '192.168.100.{}'.format(self.team)
    morse_ip = '0.0.{}.{}'.format(self.team,self.mac)
    """ Should a Routing Table be added?
    rt_table = {'II':(Ian's IP, Ian's Port),
                 'IN':(Nick's IP, Nick's Port),
                 'ID':(Deniz's IP, Deniz's Port)
                }
    """
    
    def __init__(self,Router_Address=(self.eth_ip,5280)):

        socket, msocket, AF_INET, SOCK_DGRAM = CN_Sockets.socket, CustomSockets.socket, CN_Sockets.AF_INET, CN_Sockets.SOCK_DGRAM

        self.Router_Address = Router_Address

        with socket(AF_INET,SOCK_DGRAM) as sock:
            with msocket(AF_INET,SOCK_DGRAM) as msock:
                
                sock.bind(self.eth_ip,5280)
                sock.settimeout(2.0) # 2 second timeout
                msock.bind(self.morse_ip,5280)  
                msock.settimeout(2.0) # 2 second timeout
                
                print ("UDP_Receiver started for CN_RouterReceiver at IP address {} on port {}".format(
                    Router_Address[0],Router_Address[1])
                       )

                while True:
                    try:
                        bytearray_msg, address = sock.recvfrom(1024)
                        source_IP, source_port = address
                        # Need access to routing destination
                        data = bytearray_msg.decode('utf-8')
                        destination_address = data[:2]
                        
                        print ("\n{} byte message received from ip address {}, port {}:".format(len(bytearray_msg),source_IP,source_port))
                        print ("\n"+bytearray_msg.decode("UTF-8"))

                        
                    """ IF routing table 
                        destination_address = rt_table[destination_address]
                        ENDIF """ 
                        
                        msock.sendto(bytearray_msg, destination_address)
                        print ("\n{} byte message routed via morsenet")
            

                    except timeout:
                        print (".",end="",flush=True)
                        continue
                
                
            



            
        
