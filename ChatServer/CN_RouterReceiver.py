import CN_Sockets
import RouterSocket

class CN_RouterReceiver(object):
    
    group = 'I'
    mac = 'T'
    
    router_eth_ip = {"I":"192.168.100.73",
                     "E":"192.168.100.50",
                     "T":"192.168.100.84",
                     "R":"192.168.100.82"
                    }
    
    def __init__(self,Router_Address=("192.168.100.73",5073)):

        socket, rtsocket, AF_INET, SOCK_DGRAM, timeout = CN_Sockets.socket, RouterSocket.RouterSocket, CN_Sockets.AF_INET, CN_Sockets.SOCK_DGRAM, CN_Sockets.timeout

        self.Router_Address = Router_Address

        with socket(AF_INET,SOCK_DGRAM) as sock:
            with rtsocket(AF_INET,SOCK_DGRAM) as rtsock:
                sock.bind(Router_Address)
                sock.settimeout(2.0) # 2 second timeout
                rtsock.bind(("0.0.73.73","69"))
                #rtsock.settimeout(2.0) # 2 second timeout
                
                print ("UDP_Receiver started for CN_RouterReceiver at IP address {} on port {}".format(
                    Router_Address[0],Router_Address[1])
                       )

                while True:
                    try:
                        # We assume the bytearray CN_RouterSender sends on the ethernet is the same as what CN_RouterReceiver receives on ethernet
                        # Hence the variable name bytearray_(ipheader_udpheader_msg)
                        bytearray_ipheader_udpheader_msg, other_router_address = sock.recvfrom(1024)
                        source_IP, source_port = other_router_address
                        
                        ipheader_udpheader_msg = bytearray_ipheader_udpheader_msg.decode('utf-8')
                        
                        # --- relies on IP/UDP Protocal written by Hill et al --- #
                        ipheader = ipheader_udpheader_msg[:7] # eg.'EA' + 'IB' + 'E' + 'EA'
                        udpheader = ipheader_udpheader_msg[7:9] # eg. 'B' + 'C'
                        msg = ipheader_udpheader_msg[9:]
                        dst_ip, src_ip = ipheader[:2], ipheader[2:4] # ipheader example: 'EA' + 'IB' + 'E' + 'EA' where 'EA' is ip_to, 'IB' is ip_from
                        dst_port, src_port = udpheader # udpheader example: 'BC' where B udp_to, C udp_from
                                               
                        # destination/to address should be in the same format that CN_RouterSocket.recvfrom returns
                        # (ip_to, udp_to) format
                        dst_address = (dst_ip, dst_port)
                        print ("Expected Destination Address Format: " + str(("II", "E")))
                        print ("Output Destination Address: " + str(dst_address))

                        # source/from address assume to adhere to CN_RouterSocket.recvfrom returns
                        # (ip_from, udp_from) format
                        src_address = (src_ip, src_port)
                        print ("Expected source address format: " + str(("II", "E")))
                        print ("Output source address format: " + str(src_address))

                        print ("\n{} byte message received via the ethernet from ip address {}, port {}:".format(len(bytearray_msg),source_IP,source_port))
                        print ("\n"+bytearray_ipheader_udpheader_msg.decode("UTF-8"))
                        
                        bytearray_msg = msg.encode()
                        rtsock.sendto(bytearray_msg, dst_address, src_address)
                        print ("\n{} byte message routed via morsenet")
            

                    except timeout:
                        # standby_display(".") # print standby dots on the same line
                        continue
                
if __name__ == '__main__':
    router = CN_RouterReceiver()



            
        
