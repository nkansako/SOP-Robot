import socket

def server():
    s = socket.socket()         # Create a socket object
    #host = socket.gethostname() # Get local machine name
    host = ""
    port = 12345                # Reserve a port for your service.
    s.bind((host, port))        # Bind to the port
    print("halloo")
    s.listen(5)                 # Now wait for client connection.
    while True:
        c, addr = s.accept()     # Establish connection with client.
        print('Got connection from', addr)
        message = 'Thank you for connecting'
        message = message.encode()
        c.send(message)
    c.close() 

def main():
    server()
    
if __name__ == "__main__":
    main()