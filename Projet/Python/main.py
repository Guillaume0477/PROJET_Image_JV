import Calibrage
import Track
import DetectParams
import Py_utils as utils
import cv2
import matplotlib.pyplot as plt
import numpy as np

def main():
    #Config cam
    cap = cv2.VideoCapture(0)
    play = True


    colorHand, [squareOffset, squareSize] = Calibrage.HandCalibrate(cap)
    found = True


    while play :

        #Get the frame
        ret,frame = cap.read()
        sFrame = np.shape(frame)
        tolerance = 30

        xmin = squareOffset[0]
        xmax = squareOffset[0] + squareSize[0]
        ymin = squareOffset[1]
        ymax = squareOffset[1] +  squareSize[1]


        segR = np.array(cv2.inRange(frame[xmin:xmax,ymin:ymax,0], colorHand[0]-tolerance, colorHand[0]+tolerance))
        segR *= np.array(cv2.inRange(frame[xmin:xmax,ymin:ymax,1], colorHand[1]-tolerance, colorHand[1]+tolerance))
        segR *= np.array(cv2.inRange(frame[xmin:xmax,ymin:ymax,2], colorHand[2]-tolerance, colorHand[2]+tolerance))
        
        segR = utils.Cleaning(segR)
        color = utils.UpdateColor(segR, frame[xmin:xmax, ymin:ymax, :])
        squareOffset, squareSize = Track.trackHand(segR, squareOffset, squareSize, sFrame)


        if (np.sum(segR)/255 < 0.1*squareSize[0]*squareSize[1]):
            if squareSize[0] == 100:
                squareOffset, squareSize = Track.LookForHand(sFrame)
            found = False
        else :
            found = True

        if found :
            Params = DetectParams.getParameters(frame, segR)

            segR[int(Params[2][0]), :] = 127
            segR[:, int(Params[2][1])] = 127
        
        
        frame[xmin:xmax,ymin:ymax,0] = segR
        frame[xmin:xmax,ymin:ymax,1] = segR
        frame[xmin:xmax,ymin:ymax,2] = segR
        




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