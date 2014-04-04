import CN_Sockets
import CustomSocket
import time

class UDP_Server(object):
    

    
    def __init__(self,IP="0.0.73.68",port=69):

        socket, AF_INET, SOCK_DGRAM, timeout = CustomSocket.CustomSocket, CN_Sockets.AF_INET, CN_Sockets.SOCK_DGRAM, CN_Sockets.timeout
        
        with socket(AF_INET, SOCK_DGRAM) as sock:
            sock.bind((IP,port))
            sock.settimeout(2.0) # 2 second timeout
            
            print ("UDP Server started on IP Address {}, port {}".format(IP,port))
            
            while True:
                try:
                    data = sock.recvfrom(1024)
                    time.sleep(1.5)
                    if not data:
                        raise timeout
                    
                    bytearray_msg, address = sock.recvfrom(1024)
                    source_IP, source_port = address
                    
                    print ("\nMessage received from ip address {}, port {}:".format(
                        source_IP,source_port))
                    print (bytearray_msg.decode("UTF-8"))
        

                except timeout:
##                    print (".",end="",flush=True)
                    continue
                
                
            



            
        
