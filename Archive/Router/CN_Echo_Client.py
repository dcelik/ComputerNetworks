
import CN_Sockets # CN_Sockets adds ability to interrupt "while True" loop with ctl-C
    

            
class CN_Echo_Client(object):
    """ Computer Networks Chapter 4: Sockets.  UDP Client example. """ 
    
    
    def __init__(self,Server_Address=("127.0.0.1",5280)):

        socket, AF_INET, SOCK_DGRAM = CN_Sockets.socket, CN_Sockets.AF_INET, CN_Sockets.SOCK_DGRAM

        self.Server_Address = Server_Address

        with socket(AF_INET,SOCK_DGRAM) as sock:

            sock.settimeout(2.0) # 2 second timeout
          
            
            print ("UDP_Client started for CN_Echo_Server at IP address {} on port {}".format(
                Server_Address[0],Server_Address[1])
                   )

    
            while True:
                
                str_message_to_send = input("Enter message to send to echo server:\n")

                if not str_message_to_send:
                    break
                
                sent_bytearray_message = bytearray(str_message_to_send,encoding="UTF-8")

                bytes_sent = sock.sendto(sent_bytearray_message, self.Server_Address)
                
                print ("{} bytes sent".format(bytes_sent))

                address_received = ("a.b.c.d",(-1))

                while Server_Address != address_received:
                    try:
                        bytearray_message_received, address_received = sock.recvfrom(1500)
                        if address_received != self.Server_Address:
                            print( "\n message from {} ignored".format(address_received))
                    except timeout:
                        print (".",end="",flush=True)
                        continue
                str_message_received = bytearray_message_received.decode("UTF-8")
                print ("\n{} bytes received".format(len(bytearray_message_received)))
                print ("message received:\n{}".format(str_message_received))
                
                

        print ("UDP_Client ended")

    



               
    
                
                
                
            



            
        
