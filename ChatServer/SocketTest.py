from CustomSocket import *
# Ian's

sock = CustomSocket()
sock.bind(("0.0.73.73",69))

while True:
    try:
        bytearray_msg, address = sock.recvfrom(1024)
        print ("\n{} byte array msg received from ip address {}, port {}".format(
            len(bytearray_msg), address[0], address[1]))
        print ("\n{}"+bytearray_msg.decode("UTF-8"))
    except:
        os.sys.stdout.write(".")
        continue
    
