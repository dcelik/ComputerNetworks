import sys
import os
import GlobalVars as g
import threading
sys.path.insert(0,os.path.join(os.getcwd(), os.pardir)); # Add MAC_Identifier location to path
import MAC_Identifier as MAC
sys.path.insert(0,os.path.join(os.getcwd(), os.pardir, "TransmissionModule"));
import transmit as t;
import queuedMonitor as r;

from CustomSocket import CustomSocket

class RouterSocket(CustomSocket):
    def __init__(self,family = 2, protocol = 2, router_mac="T",verbose=False,debug=True):
        CustomSocket.__init__(self,family,protocol,router_mac,verbose,debug)
        self.macDict = {"II":"I",
                        "IR":"R",
                        "IN":"N",
                        "ID":"D",
                        }
    def sendto(self,msg,destination_address, source_address):
        """ Router Should "forward" a message on, meaning it should not add it's
        own ip/udp address to the header. Thus, a source_address of the original sender is needed
        """
        # NOTE: Staying in Morse (II) vs pubIP (0.0.73.73)
        
        if not self.validIPAndPort:
            print("Error: Invalid IP and port or socket has not been bound with an IP and port: message not sent!");
            return;
        
        to_ip_addr, to_port = destination_address
        from_ip_addr, from_port = source_address
        msg = msg.decode("utf-8"); #Convert from bytearray to a string for ease of operation

        # Assemble UDP package
        udp_package = to_port + from_port + msg;

        # Assemble IP package
        ip_header = to_ip_addr + from_ip_addr + self.protocol_identifier + t.base36encode(len(udp_package));
        ip_package = ip_header + udp_package;

        # Assemble MAC package
        mac_to = self.macDict[to_ip_addr]
        mac_from = self.macDict[from_ip_addr]
        
        # Send the message
        t.sendMessage(mac_to,mac_from,ip_package);

    def recvfrom(self, buflen):
        # copy code from routerRecvFrom (below)
        data = baseRecv(buflen);
        if data is not None:
            message = data[0]; 

            mac_header = data[1];
            ip_header = data[2];
            udp_header = data[3];

            ip_to = ip_header[0];
            ip_from = ip_header[1];
            udp_to = udp_header[0];
            udp_from = udp_header[1];

            bytearray_msg = bytearray(message, encoding="utf-8")

            return bytearray_msg, (ip_from,udp_from) , (ip_to,udp_to), ip_header, udp_header; 
        else: return None;
  
  
            
  
