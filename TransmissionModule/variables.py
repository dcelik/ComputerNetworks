"""
variables.py
------------
Author: Nick Francisci
Purpose: To provide one central location to store global variables for the program
Status: Tested and Working 2-17-14
"""


blink_time = .08;    #Time given to one blink for transmission
one_baud = int(1/blink_time);                   #Number of pulses required for transmission to occur at 1 baud
header_pulse = '11110';     #Binary string to indicate start of message according to CompNet Datalink Standards
stop_pulse = '10111010111010';                    #Binary string representing morse code "+" to establish where message ends according CompNet Datalink Standards
group_code = 'I';                                 #Single char representing transmission group code "I"
origin = 'N';                                     #Single char representing name of sender
dest = 'R';                                       #Single char representing name of recipient
func = 'A';                                       #Single char representing function of message

charToBinaryDict = { "A":"101110",
              "B":"1110101010",
              "C":"111010111010",
              "D":"11101010",
              "E":"10",
              "F":"1010111010",
              "G":"1110111010",
              "H":"10101010",
              "I":"1010",
              "J":"10111011101110",
              "K":"1110101110",
              "L":"1011101010",
              "M":"11101110",
              "N":"111010",
              "O":"111011101110",
              "P":"101110111010",
              "Q":"11101110101110",
              "R":"10111010",
              "S":"101010",
              "T":"1110",
              "U":"10101110",
              "V":"1010101110",
              "W":"1011101110",
              "X":"111010101110",
              "Y":"11101011101110",
              "Z":"111011101010",
              "1":"101110111011101110",
              "2":"1010111011101110",
              "3":"10101011101110",
              "4":"101010101110",
              "5":"1010101010",
              "6":"111010101010",
              "7":"11101110101010",
              "8":"1110111011101010",
              "9":"111011101110111010",
              "0":"11101110111011101110",
              " ":"000000",
              "+":"10111010111010",
              ".":"101110101110101110",
              ",":"11101110101011101110",
              "?":"1010111011101010",
              "'":"10111011101110111010",
              "!":"11101011101011101110",
              "/":"11101010111010",
              "(":"1110101110111010",
              ")":"11101011101110101110",
              "&":"101110101010",
              ":":"111011101110101010",
              ";":"111010111010111010",
              "=":"11101010101110",
              "-":"1110101010101110",
              "_":"101011101110101110",
              "\"":"1011101010111010",
              "$":"101010111010101110",
              "@":"101110111010111010"}
binaryToCharDict = {v:k for(k,v) in charToBinaryDict.items()}
tolerance = .9
