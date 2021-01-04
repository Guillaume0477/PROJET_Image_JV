import Calibrage
import Track
import cv2
import matplotlib.pyplot as plt
import numpy as np

def main():
    #Config cam
    cap = cv2.VideoCapture(0)
    play = True


    colorHand, [squareOffset, squareSize] = Calibrage.HandCalibrate(cap)


    while play :
        #Get the frame
        ret,frame = cap.read()

        tolerance = 60

        xmin = squareOffset[0]
        xmax = squareOffset[0] + squareSize[0]
        ymin = squareOffset[1]
        ymax = squareOffset[1] +  squareSize[1]


        segR = np.array(cv2.inRange(frame[xmin:xmax,ymin:ymax,0], colorHand[0]-tolerance, colorHand[0]+tolerance))
        segR *= np.array(cv2.inRange(frame[xmin:xmax,ymin:ymax,1], colorHand[1]-tolerance, colorHand[1]+tolerance))
        segR *= np.array(cv2.inRange(frame[xmin:xmax,ymin:ymax,2], colorHand[2]-tolerance, colorHand[2]+tolerance))

        frame[xmin:xmax,ymin:ymax,0] = segR
        frame[xmin:xmax,ymin:ymax,1] = segR
        frame[xmin:xmax,ymin:ymax,2] = segR
        
        squareOffset, squareSize = Track.trackHand(segR, squareOffset, squareSize, np.shape(frame))

        #Detect user quit command
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            play = False

        #Show the frame
        cv2.imshow('Capture Video', frame)

    #Destroy windows
    cap.release()
    cv2.destroyAllWindows()
    return 0


main()