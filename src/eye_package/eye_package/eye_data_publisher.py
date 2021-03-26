import rclpy

import socket

from rclpy.node import Node

from std_msgs.msg import Float32
from std_msgs.msg import Float32MultiArray

ADDRESS = "127.0.0.1"
UDP_PORT = 4242

class EyeDataPublisherHorizontal(Node):

    def __init__(self):
        super().__init__('eye_data_publisher_horizontal')
        self.publisher_ = self.create_publisher(Float32MultiArray, 'move_eye_horizontal', 10)
        timer_period = 1.0
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.left = True
        self.direction = 1.0
        self.x = 0.0
        self.y = 0.0

    def timer_callback(self):
        #msg = Float32()
        #print("moikka")
        msg1 = Float32MultiArray()
        msg1.data = [self.x, 1.0]
        msg2 = Float32MultiArray()
        msg2.data = [self.y, -1.0]
        #server()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #ADDRESS = ""
        s.bind(("10.0.2.15", UDP_PORT))
        #s.listen(1)
        print("socket opened")

        counter = 0
        counterlimit = 10

        while True:
            #c, _ = s.accept()
            
            #print("inloop")
            data = s.recv(48)
            #print(data)
            data = data.decode().split(":")
            counter += 1

            if counter == counterlimit:
                counter = 0
                break
            else:
                continue

        s.close()
        #data = receive_tcp(ADDRESS, UDP_PORT)
        x = float(data[0])
        y = float(data[1])
        #print(data)
        self.x = x
        self.y = y
        self.publisher_.publish(msg1)

        self.get_logger().info('Publishing: %f' % msg1.data[0])

        self.publisher_.publish(msg2)

        self.get_logger().info('Publishing: %f' % msg2.data[0])
        

def receive_udp(address, port):
    # create UDP socket
    print("hei")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # You turned the message in to str in previous function. Turn it back to bytes
    #msg = message.encode()
    # send given message to given address and port using the socket.
    s.bind((address, port))
    #s.connect((address,port))
    print(s)
    finaldata = []
    inLoop = 1
    while(inLoop):
        print("halloo")
        # receive data from socket
        data, _ = s.recvfrom(48)
        print(data)
        # Data you receive is in bytes format. Turn it to string with .decode() command
        data_decode = data.decode()
        # print received data
        print(data_decode)
        # if received data contains the word 'QUIT' break the loop
        
        if "QUIT" in data_decode:
            inLoop = 0
        else:
            finaldata.append(float(data_decode))

    s.close()
   # msg = float(data_decode)
    print("boo")
    return finaldata

def receive_tcp(address, port):
    print("tässä")
    s = socket.socket()
    host = ""
    port = 12345
    s.bind((host, port))
    s.listen(5)
    inLoop = 1
    while(inLoop):
        print("loopissa")
        c, addr = s.accept()
        msg = c.recv(48).decode()
        data = msg.split(":")
        s.close()
        print("hello")
        return data

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
        c.send('Thank you for connecting')
    c.close()                # Close the connection

def main(args=None):
    rclpy.init(args=args)

    eye_data_publisher_horizontal = EyeDataPublisherHorizontal()

    rclpy.spin(eye_data_publisher_horizontal)

    eye_data_publisher_horizontal.destroy_node()

    rclpy.shutdown()

if __name__ == '__main__':
    main()