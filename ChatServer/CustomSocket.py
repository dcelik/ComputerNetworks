import sys
import os
import threading
sys.path.insert(0,os.path.join(os.getcwd(), os.pardir)); # Add MAC_Identifier location to path
import MAC_Identifier as MAC
sys.path.insert(0,os.path.join(os.getcwd(), os.pardir, "TransmissionModule"));
import transmit as t;
import queuedMonitor as r;



class CustomSocket:
    # Associate variables with names so they can be retrived by server
    AF_INET = 2;
    SOCK_DGRAM = 2;
    timeout = -1;   
  
    def __init__(self,family, protocol, router_mac="T",verbose=False, test_init=True):
        """ Initialize a CustomSocket instance """
    

        # Setup booleans to validate that socket is used correctly
        self.validFamilyAndProtocol = False;
        self.validIPAndPort = False;
        # Setup MAC Data
        self.my_mac = MAC.my_ad;
        if self.my_mac != router_mac:
            self.macDict = dict();
            self.macDict['router_mac']  = router_mac;
    
        self.verbose = verbose;

    # ------ Set Up Family and Protocol ------ #
        if family!=2:   #AF_INET
            print("Sorry, this address family is not currently supported!");
        else:
            self.family = 2;

        if protocol!=2: #UDP
            print("Sorry, this sending protocol is not currently supported!");
        else:
            self.protocol = 2;

        #Our "UDP" imports (importing our Morse implementation of UDP)
        if protocol==2: 
            self.validFamilyAndProtocol = True;
            self.protocol_identifier = 'E'; #The standard defined base 36 char designating UDP
        


        if test_init: self.bind(("0.0.73.73","69"));

        
    def bind(self, address):
        """ Start a socket listening for messages addressed to the parent class. """

        address = self.morseToPubIP(address);

        # Returns with error if inputs are invalid
        if not self.validFamilyAndProtocol:
            print("Error: Invalid family and protocol or family and protocol are not initialized: socket not bound!");
            return;

        self.my_ip_addr = address[0];
        self.my_port = address[1];
        self.validIPAndPort = True;

        #Starts a monitor function on a new thread that queues messages as they are recieved

        self.qt = threading.Thread(target=r.monitor);
        self.qt.start(); #This may cause a memory leak - unsure.
        
        if self.verbose:
            print("Socket bound. Your IP is " + self.my_ip_addr + ". Your port is " + self.my_port);

    
    def pubIPToMorse(self, ip_from_morse, port_from_morse):
        """ Converts and address in the Morse letter IP and Port to letters for movement up to the app layer. """
                
        ip_from_str = "0.0.";
        ip_from_str += str(ord(ip_from_morse[0])) + "." +  str(ord(ip_from_morse[1]));
        port_from_str = str(ord(port_from_morse));
        
        return ip_from_str, port_from_str;
    
    def morseToPubIP(self, address):
        """ Converts an address in the standard IP:Port format to letters for transmission on our morse layer. """

        new_address = address[0].split(".");
        new_address.append(address[1]);
        new_address = [int(letter_code) for letter_code in new_address];
    
        ip_addr = chr(new_address[2]) + chr(new_address[3]);
        port = chr(new_address[4]);
    
        return ip_addr, port;
    
    def settimeout(self, timeout):
        """ Sets a message timeout: the timeout is currently unused """
        self.timeout = timeout;

    def sendto(self,msg,address):
        """ Assembles a message and sends it with the down-stack implementation. """

        if not self.validIPAndPort:
            print("Error: Invalid IP and port or socket has not been bound with an IP and port: message not sent!");
            return;

        to_ip_addr = address[0];
        to_port = address[1];
        msg = msg.decode("utf-8"); #Convert from bytearray to a string for ease of operation

        # Assemble UDP package
        udp_package = to_port + self.my_port + msg;

        # Assemble IP package
        ip_header = to_ip_addr + self.my_ip_addr + self.protocol_identifier + t.base36encode(len(udp_package));
        ip_package = ip_header + udp_package;

        # Assemble MAC package
            # First check to see if the MAC of the recieving IP is known, if not address message to router
        if macDict[to_ip_addr] is not None: mac_to = macDict[to_ip_addr];
        else: mac_to = macDict['router_mac'];   # This only works if you're not the router...
            # Then assemble the remainder of the MAC package
        mac_from = my_mac;
        # Send the message
        t.sendMessage(mac_to,mac_from,ip_package);

    def baseRecv(self, buflen):
        """ 
        Checks the threaded monitoring function to see if any messages have been recorded. 
        Then it checks to see if the message is addressed to this MAC, IP, and port and returns
        if it is. In the process it records the MAC address of the sending computer into a dict
        for future use. Returns the message with all recorded header data for further processing.

        """

        # Attempts to retrieve a message from the queue initilized in bind, returns None if there are no messages
        data = r.popMessage();  

        # Checks to see if a message was retrieved
        if data is None:
            return None; # Not certain if this is the correct return for this...
        else:
            dest_mac = data[0];
            source_mac = data[1];
        length = data[2];
        payload = data[3];
        mac_header = dest_mac+source_mac+length;

        ip_header = payload[:7];
        udp_header = payload[7:9];
        message = payload[9:];

        # If the message is not addressed to this computer's MAC, discard the message
        if dest_mac != self.my_mac: return None;

        if (buflen<len(message)): return None;
        else: return message, mac_header, ip_header, udp_header;

    def recvfrom(self, buflen):
        """ The recieve function to be used by standard applications. """

        data = baseRecv(buflen);
        if data is not None:
            message = data[0];
            mac_header = data[1];
            ip_header = data[2];
            udp_header = data[3];

            udp_to = udp_header[0];
            mac_from = mac_header[1];
            ip_from = ip_header[1];
            udp_from = udp_header[1];


            # Add the MAC to the MAC dictionary if it is not already recorded.
            if macDict[ip_from] is None: macDict[ip_from] = mac_from;

            # If the message is not addressed to this computer's IP, discard the message (should be redudant with MAC)
            if ip_to != self.my_ip_addr: return None;

            # If the message is not addressed to this application's port, discard the message
            if udp_to != self.my_port: return None;

            return message, pubIPToMorse(ip_from,udp_from); 
        else: return None;
