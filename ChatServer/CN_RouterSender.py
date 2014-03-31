
import CN_Sockets # CN_Sockets adds ability to interrupt "while True" loop with ctl-C
import RouterSocket
import os

class CN_RouterSender:
    """ Computer Networks Chapter 4: Sockets.  UDP Client example. """ 

    group = 'I'
    mac = 'T'
    
    router_eth_ip = {"I":"192.168.100.73",
                     "E":"192.168.100.50",
                     "T":"192.168.100.84"
                    }

    # When Connecting to Olin Network, use the ip given by eth1 of ifconfig
    def __init__(self,Router_Address=("10.26.8.27",5073)):

        socket, rtsocket, AF_INET, SOCK_DGRAM, timeout = CN_Sockets.socket, RouterSocket.RouterSocket, CN_Sockets.AF_INET, CN_Sockets.SOCK_DGRAM, CN_Sockets.timeout

        self.Router_Address = Router_Address
        
        with socket(AF_INET,SOCK_DGRAM) as sock:
            with rtsocket(AF_INET,SOCK_DGRAM) as rtsock:
                sock.bind(Router_Address)
                sock.settimeout(2.0) # 2 second timeout
                rtsock.bind(("0.0.73.84","69"))
                #rtsock.settimeout(2.0) # 2 second timeout
                
                print ("UDP_Sender started for CN_RouterSender at IP address {} on port {}".format(
                    Router_Address[0],Router_Address[1])
                       )
                
                while True:
                    try:
                        # Receive Messages from LAN
                        # NOTE: Addresses are STAYING in Morseformat
                        data = rtsock.recvfrom(1024);
                        if not data: raise timeout;

                        bytearray_msg, source_address, destination_address, ipheader, udpheader = data # special router recvfrom function
                        source_IP, source_port = source_address
                        destination_IP, destination_port = destination_address
                        print ("ERROR:"+destination_address[0]+destination_address[1])
                        print ("\n{} byte message received from ip address {}, port {}:".format(len(bytearray_msg),source_IP,source_port))
                        print ("\n"+bytearray_msg.decode("UTF-8"))

                        # destination_IP example: IA, where I is group, A is mac
                        print(destination_IP)
                        destination_group, destination_mac = destination_IP

                        if self.group == destination_group:
                            # Route to own group over morsenet
                            # Address Resloution Protocol
                            rtsock.sendto(bytearray_msg, destination_address, source_address)
                            print ("\n{} byte message routed via morsenet")
                        else:
                            # Route to other group's router over ethernet
                            bytearray_ipheader_udpheader_msg = bytearray(ipheader + udpheader, encoding='UTF-8') + bytearray_msg
                            dst_group_router = self.router_eth_ip[destination_group]
                            sock.sendto(bytearray_ipheader_udpheader_msg, dst_group_router)
                            print ("\n{} byte message routed via ethernet")

                    except timeout:
                        os.sys.stdout.write(".")
                        continue                
                

        print ("UDP_Client ended")
