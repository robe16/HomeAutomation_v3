import socket

# creating a socket object
s = socket.socket(socket.AF_INET,
                  socket.SOCK_STREAM)

# get local Host machine name
host = socket.gethostname()
port = 1616

# bind to pot
s.bind((host, port))

# Que up to 5 requests
s.listen(5)

while True:
    # establish connection
    (clientSocket, address) = s.accept()
    data = clientSocket.recv()
    #
    print("got a connection from: " + str(address))
    print("message as follows: " + data)
    #
    STRresponse=""
    clientSocket.send(STRresponse.encode('ascii'))
    #clientSocket.close()