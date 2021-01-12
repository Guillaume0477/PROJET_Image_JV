import Calibrage
import Track
import DetectParams
import Segment
import Py_utils as utils
import cv2
import matplotlib.pyplot as plt
import numpy as np
from math import floor


def main():
    #Config cam
    cap = cv2.VideoCapture(0)
    play = True

    #Hand calibration
    colorHand, hueValue, [squareOffset, squareSize] = Calibrage.HandCalibrate(cap)
    found = True

    # seginter = np.ones(squareSize)

    while play :
        
        #Get the frame
        ret,frame = cap.read()
        sFrame = np.shape(frame)

        #Bounds of the square
        xmin = squareOffset[0]
        xmax = squareOffset[0] + squareSize[0]
        ymin = squareOffset[1]
        ymax = squareOffset[1] +  squareSize[1]
        bounds = [xmin, xmax, ymin, ymax]

        #Segmentation of the hand inside the square according to hsv
        segR = Segment.getHSVColorSeg(frame, bounds, hueValue)

        # # Cleaning of the space to better segment hand
        #segR = utils.Cleaning(segR)

        # # Tests using distance transform
        # seginter = cv2.distanceTransform(segR, cv2.DIST_L2, 3)
        # seginter = seginter/np.max(seginter)*255
        # print(squareSize, np.shape(segR))
        # seginter = np.multiply(segR/255, seginter)
        
        #Tracking of the hand (moving/increasing/decresing the size of the square)
        squareOffset, squareSize = Track.trackHand(segR, squareOffset, squareSize, sFrame)

        #Check if the hand is still found inside the square
        if (np.sum(segR)/255 < 0.1*squareSize[0]*squareSize[1]):
            if squareSize[0] == 100:
                squareOffset, squareSize = Track.LookForHand(sFrame)
            found = False
        else :
            found = True

        #If hand has been found
        if found :
            #Get the parameters of the position and shape of the hand
            Params = DetectParams.getParameters(frame, segR)

            #Display gravity center on screen
            segR[int(Params[2][0]), :] = 127
            segR[:, int(Params[2][1])] = 127

            # # Tests to update hsv channel while playing to be adaptative
            # hueValue = utils.UpdateColor(segR, frame[xmin:xmax, ymin:ymax, :])

        
        # Display the segmentation on screen 
        frame[xmin:xmax,ymin:ymax,0] = segR
        frame[xmin:xmax,ymin:ymax,1] = segR
        frame[xmin:xmax,ymin:ymax,2] = segR
        
        # # Tests due to distance transform
        # seginter = np.zeros(squareSize)
        # diff = np.array(squareSize) - np.shape(segR)
        # print(diff, squareSize, np.shape(segR))
        # if diff[0] >= 0 :
        #     seginter[floor(diff[0]/2):squareSize[0]-floor(diff[0]/2), floor(diff[1]/2):squareSize[1]-floor(diff[1]/2)] = segR
        # else :
        #     diff = -diff
        #     segRs = np.shape(segR)
        #     seginter = segR[floor(diff[0]/2):segRs[0]-floor((diff[0]+1)/2), floor(diff[1]/2):segRs[1]-floor((diff[1]+1)/2)]


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