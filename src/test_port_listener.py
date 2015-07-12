import socket
#import server
#import port_listener

def testPort(data):
    #port_listener.listen()
    #server.main()
    speak(data)
    #

def speak(STRresponse):
    # creating a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind to pot
    #s.connect((socket.gethostname(), 1616))
    s.connect(('localhost', 1616))

    while True:
        #
        try:
            s.sendall(STRresponse)
            # Look for the response
            #amount_received = 0
            #amount_expected = len(message)
            #
            #while amount_received < amount_expected:
            x = s.recv(4096)
                #amount_received += len(data)
            print ("Response recieved: "+x)
        finally:
            # Clean up the connection
            s.close()

print ("*****************************************")
print ("************* Test 1: Socket*************")
print ("*****************************************")
msg = "This is the test message"
print (msg)
testPort(msg)
print ("*****************************************")
print ("****************TEST  END****************")
print ("*****************************************")