
import CN_Sockets # CN_Sockets adds ability to interrupt "while True" loop with ctl-C
import RouterSockets    

           
class CN_RouterSender(object):
    """ Computer Networks Chapter 4: Sockets.  UDP Client example. """ 

    group = 'I'
    mac = 'T'
    
    router_eth_ip = {"I":"192.168.100.73",
                     "E":"192.168.100.50",
                     "T":"192.168.100.84"
                    }

    def __init__(self,Router_Address=(self.router_eth_ip[self.group],73)):

        socket, rtsocket, AF_INET, SOCK_DGRAM = CN_Sockets.socket, RouterSockets.socket, CN_Sockets.AF_INET, CN_Sockets.SOCK_DGRAM

        self.Router_Address = Router_Address

        with socket(AF_INET,SOCK_DGRAM) as sock:
            with rtsocket(AF_INET,SOCK_DGRAM) as rtsock:
                
                sock.bind(self.eth_ip,73)
                sock.settimeout(2.0) # 2 second timeout
                rtsock.bind(self.morse_ip,69)  
                rtsock.settimeout(2.0) # 2 second timeout
                
                print ("UDP_Sender started for CN_RouterSender at IP address {} on port {}".format(
                    Router_Address[0],Router_Address[1])
                       )
                
                while True:
                    try:
                        # Receive Messages from LAN
                        bytearray_msg, source_address, destination_address, ipheader, udpheader = rtsock.recvfrom(1024) # special router recvfrom function
                        source_IP, source_port = source_address
                        destination_IP, destination_port = destination_address

                        print ("\n{} byte message received from ip address {}, port {}:".format(len(bytearray_msg),source_IP,source_port))
                        print ("\n"+bytearray_msg.decode("UTF-8"))

                        # destination_IP example: IA, where I is group, A is mac
                        destination_group, destination_mac = destination_IP

                        if self.group == destination_group:
                            # Route to own group over morsenet
                            # Address Resloution Protocol
                            rtsock.sendto(bytearray_msg, destination_address)
                            print ("\n{} byte message routed via morsenet")
                        else:
                            # Route to other group's router over ethernet
                            bytearray_ipheader_udpheader_msg = bytearray(ipheader + udpheader, encoding='UTF-8') + bytearray_msg
                            dst_group_router = self.router_eth_ip[destination_group]
                            sock.sendto(bytearray_ipheader_udpheader_msg, dst_group_router)
                            print ("\n{} byte message routed via ethernet")

                    except timeout:
                        print (".",end="",flush=True)
                        continue                
                

        print ("UDP_Client ended")
