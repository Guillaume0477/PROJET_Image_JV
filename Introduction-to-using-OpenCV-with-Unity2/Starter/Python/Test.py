import numpy as np
import cv2
import math
import socket
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 5065

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

last = []

# Open Camera
try:
    default = 0 # Try Changing it to 1 if webcam not found
    capture = cv2.VideoCapture(default)
except:
    print("No Camera Source Found!")

while capture.isOpened():
    


    key = cv2.waitKey(1)
    if key == ord('j'):
        last = []
        sock.sendto( ("JUMP!").encode(), (UDP_IP, UDP_PORT) )
        print("_"*10, "Jump Action Triggered!", "_"*10)

    if key == ord('f'):
        last = []
        sock.sendto( ("FIRE!").encode(), (UDP_IP, UDP_PORT) )
        print("_"*10, "Fire Action Triggered!", "_"*10)


    # Capture frames from the camera
    ret, frame = capture.read()
    

    cv2.imshow("Full Frame", frame)



capture.release()
cv2.destroyAllWindows()