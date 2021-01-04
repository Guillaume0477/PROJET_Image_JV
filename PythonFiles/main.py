import Calibrage
import cv2
import matplotlib.pyplot as plt
import numpy as np

def main():
    #Config cam
    cap = cv2.VideoCapture(0)
    play = True


    colorHand, BBoxHand = Calibrage.HandCalibrate(cap)


    while play :
        #Get the frame
        ret,frame = cap.read()

        tolerance = 60

        segR = np.array(cv2.inRange(frame[:,:,0], colorHand[0]-tolerance, colorHand[0]+tolerance))
        segR *= np.array(cv2.inRange(frame[:,:,1], colorHand[1]-tolerance, colorHand[1]+tolerance))

        segR *= np.array(cv2.inRange(frame[:,:,2], colorHand[2]-tolerance, colorHand[2]+tolerance))
        #Detect user quit command
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            play = False

        #Show the frame
        cv2.imshow('Capture Video', segR)

    #Destroy windows
    cap.release()
    cv2.destroyAllWindows()
    return 0


main()