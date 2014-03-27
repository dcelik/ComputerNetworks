import CN_Sockets
import CustomSockets

class CN_RouterReceiver(object):
    
    team = 'I'
    mac = 'R'
    router_ip = '0.0.{}.{}'.format(self.team,self.mac)

    def __init__(self,IP="127.0.0.1",port=5280):

        socket, AF_INET, SOCK_DGRAM, timeout = CN_Sockets.socket, CN_Sockets.AF_INET, CN_Sockets.SOCK_DGRAM, CN_Sockets.timeout
        
        with socket(AF_INET, SOCK_DGRAM) as sock:
            sock.bind((IP,port))
            sock.settimeout(2.0) # 2 second timeout
            
            print ("UDP Server started on IP Address {}, port {}".format(IP,port))
            
            while True:
                try:
                    bytearray_msg, address = sock.recvfrom(1024)
                    source_IP, source_port = address
                    
                    print ("\n{} byte message received from ip address {}, port {}:".format(len(bytearray_msg),source_IP,source_port))
                    print ("\n"+bytearray_msg.decode("UTF-8"))

                    lenx= sock.sendto(bytearray_msg, address)
                    print ("\n{} byte message echoed")
        

                except timeout:
                    print (".",end="",flush=True)
                    continue
                
                
            



            
        
