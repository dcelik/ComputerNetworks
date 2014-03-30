import CN_Sockets
import RouterSocket

class CN_RouterReceiver(object):
    
    group = 'I'
    mac = 'T'
    
    router_eth_ip = {"I":"192.168.100.73",
                     "E":"192.168.100.50",
                     "T":"192.168.100.84"
                    }
    
    def __init__(self,Router_Address=(self.router_eth_ip[self.group],73)):

        socket, rtsocket, AF_INET, SOCK_DGRAM = CN_Sockets.socket, RouterSocket.socket, CN_Sockets.AF_INET, CN_Sockets.SOCK_DGRAM

        self.Router_Address = Router_Address

        with socket(AF_INET,SOCK_DGRAM) as sock:
            with rtsocket(AF_INET,SOCK_DGRAM) as rtsock:
                
                sock.bind(self.eth_ip,73)
                sock.settimeout(2.0) # 2 second timeout
                rtsock.bind(self.morse_ip,69)  
                rtsock.settimeout(2.0) # 2 second timeout
                
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
                        
                        rtsock.sendto(bytearray_msg, destination_address)
                        print ("\n{} byte message routed via morsenet")
            

                    except timeout:
                        print (".",end="",flush=True)
                        continue
                
                
            



            
        
