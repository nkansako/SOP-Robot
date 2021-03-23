import cv2
import numpy as np
import socket
cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)


UDP_PORT = 21002
ADDRESS = "127.0.0.1"
def eyetracker():
    x = 1
    y = 1
    w = 1
    h = 1
    if vc.isOpened(): # try to get the first frame
        rval, eye = vc.read()
    else:
        rval = False
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #s.bind((ADDRESS, 12345))
    s.connect((ADDRESS, 12345))
    while rval:
        #cv2.imshow("preview", eye)
        rval, eye = vc.read()
        rows, cols, _ = eye.shape
        gray_roi = cv2.cvtColor(eye, cv2.COLOR_BGR2GRAY)
        gray_roi = cv2.GaussianBlur(gray_roi, (3, 3), 0)
        _, threshold = cv2.threshold(gray_roi, 25, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
        #print(contours)
        for c in contours:
            (x, y, w, h) = cv2.boundingRect(c.astype(np.int))
            break
        #print(x,y,w,h)
        cv2.drawContours(eye, contours, 0, (0,255,0), 3)
        cv2.rectangle(eye, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.line(eye, (x + int(w/2), 0), (x + int(w/2), rows), (0, 255, 0), 2)
        cv2.line(eye, (0, y + int(h/2)), (cols, y + int(h/2)), (0, 255, 0), 2)
        coordinate = (x+int(w/2), y+int(h/2))
        cv2.circle(eye, coordinate, 1, (0,0,0), -1)

        #print(coordinate)
        
        finalx = (coordinate[0] / 960) - 1
        finaly = (coordinate[1] / 540) - 1 
        
        message1 = str(finalx)
        message2 = str(finaly)
        message = message1+":"+message2
        message = message.encode()
        s.send(message)
        #print(message)
        #cv2.imshow("Threshold", threshold)
        #cv2.imshow("gray roi", gray_roi)
        #cv2.imshow("Roi", eye)
        key = cv2.waitKey(20)
        if key == 27: # exit on ESC
            s.close()
            break
    vc.release()
    cv2.destroyWindow("preview")


def send_and_receive_udp(address, port, message):
    # create UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # You turned the message in to str in previous function. Turn it back to bytes
    msg = message.encode()
    # send given message to given address and port using the socket.
    #s.bind(("",port))
    #s.connect((address,port))
   
    s.sendto(msg, (address, port))
   
    #print(msg)
    # Loop the following
    """
    inLoop = 1
    while(inLoop):
        # receive data from socket
        data = s.recvfrom(1024)
        # Data you receive is in bytes format. Turn it to string with .decode() command
        data_decode = data[0].decode().upper()
        # print received data
        print(data_decode)
        # if received data contains the word 'QUIT' break the loop
        if "QUIT" in data_decode:
            inLoop = 0
    """
    s.close()
       
    # close the socket
    return
    
    
def client():
    s = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = 12345                # Reserve a port for your service.

    s.connect((host, port))
    print(s.recv(1024))
    s.close()                     # Close the socket when done
    
def main():
    #client()
    eyetracker()
    

if __name__ == "__main__":
    main()



