import socket

def listen():
    # creating a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind to pot
    #s.bind((socket.gethostname(), 1616))
    s.bind(('localhost', 1616))

    # Que up to 5 requests
    s.listen(5)

    while True:
        # establish connection
        (connection, client_address) = s.accept()
        #
        try:
            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(4096)
                #
                print("----")
                print("received a connection from client: " + str(client_address))
                print("message as follows: " + data)
                print("----")
                #
                if data:
                    STRresponse = "Test response"
                    connection.sendall(STRresponse)
                else:
                    break
        finally:
            # Clean up the connection
            connection.close()