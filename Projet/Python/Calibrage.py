import cv2
import numpy as np
from math import floor

import Segment
import Py_utils



# def UpdateTol(frame, hsvValue):#cap, squareOffset, squareSize):

#     sizeIm = np.shape(frame)
#     tolH = 5

#     for k in [2,5,7,10,12,50]:
#         s = Segment.getHSVColorSeg(frame, [0, sizeIm[0]-1, 0, sizeIm[1]-1], hsvValue, k)
#         # s = Py_utils.Cleaning(s)
#         cv2.imshow(str(k), s)

#     return 0


def HandCalibrate(cap):

    print("Put your hand inside the square and push 'G'")

    #Boolean for aquisition
    acq = True

    #Size and offset of the square which shoul contain hand
    squareSize = [100,100]
    squareOffset = [200,200]

    #Color parameters
    color = [0,0,0]
    hueValue = [0,0,0]
    YUV_Value =[0,0,0]

    while acq :
        #Get the frame
        ret,frame = cap.read()

        #Detect user command
        key = cv2.waitKey(1)
        
        #Aquisition of the parameters
        if key == ord('g'):
            ymin = floor(squareOffset[1] + squareSize[1]/3)
            ymax = floor(squareOffset[1] + 2*squareSize[1]/3)
            xmin = floor(squareOffset[0] + 4*squareSize[0]/7)
            xmax = floor(squareOffset[0] + 6*squareSize[0]/7)

            #Get the mean bgr color
            color = np.mean(np.mean(frame[xmin:xmax, ymin:ymax,:], axis = 0), axis = 0)

            #get the mean hsv color
            hsvValue = np.mean(np.mean(cv2.cvtColor(frame[xmin:xmax, ymin:ymax,:], cv2.COLOR_BGR2HSV), axis = 0), axis = 0)
            #tolH = UpdateTol(frame[squareOffset[0]:squareOffset[0]+squareSize[0], squareOffset[1]:squareOffset[1]+squareSize[1],:], hsvValue)
            YUV_Value = np.mean(np.mean(cv2.cvtColor(frame[xmin:xmax, ymin:ymax,:], cv2.COLOR_BGR2YUV), axis = 0), axis = 0)
            
            #Transform the color from BGR to RGB
            #color[0], color[2] = color[2], color[0]

            #Show the frame
            frame[xmin:xmax,ymin:ymax,:] = 255

            #End the calibration
            acq = False

        #Move the square left
        elif key == ord('q'):
            squareOffset[1] = max(0, squareOffset[1]-10)
        #Move the square right
        elif key == ord('d'):
            squareOffset[1] = min(squareOffset[1]+10, np.shape(frame)[1]-1-squareSize[1])
        #Move the square up
        elif key == ord('z'):
            squareOffset[0] = max(0,squareOffset[0]-10)
        #Move the square down
        elif key == ord('s'):
            squareOffset[0] = min(squareOffset[0]+10, np.shape(frame)[0]-1-squareSize[0])
        #Reduce square size
        elif key == ord('a'):
            squareSize[0] = max(100, squareSize[0]-20)
            if(squareSize[0] != squareSize[1]):
                squareSize[1] = squareSize[0]
                squareOffset[1] = min(squareOffset[1]+10, np.shape(frame)[1]-1-squareSize[1])
                squareOffset[0] = min(squareOffset[0]+10, np.shape(frame)[0]-1-squareSize[0])
        #Increase square size
        elif key == ord('e'):
            squareSize[0] = np.min([squareSize[0]+20, np.shape(frame)[0]-1, squareSize[1]+20, np.shape(frame)[1]-1])
            if(squareSize[0] != squareSize[1]):
                squareSize[1] = squareSize[0]
                squareOffset[1] = max(0, squareOffset[1]-10)
                squareOffset[0] = max(0,squareOffset[0]-10)
            if (squareOffset[1] + squareSize[1] >= np.shape(frame)[1]):
                squareOffset[1] -=10
            if (squareOffset[0] + squareSize[0] >= np.shape(frame)[0]):
                squareOffset[0] -=10
            

        ymin = floor(squareOffset[1] + squareSize[1]/3)
        ymax = floor(squareOffset[1] + 2*squareSize[1]/3)
        xmin = floor(squareOffset[0] + 4*squareSize[0]/7)
        xmax = floor(squareOffset[0] + 6*squareSize[0]/7)
        

        #Show the frame
        frame[squareOffset[0]:squareOffset[0]+squareSize[0],squareOffset[1],:] = 255
        frame[squareOffset[0]:squareOffset[0]+squareSize[0],squareOffset[1]+squareSize[1],:] = 255
        frame[squareOffset[0],squareOffset[1]:squareOffset[1] + squareSize[1],:] = 255 
        frame[squareOffset[0]+squareSize[0],squareOffset[1]:squareOffset[1] + squareSize[1],:] = 255 
        frame[xmin:xmax,ymin:ymax,:] = 255


        cv2.imshow('Calibrate your hand', frame)

    # #Destroy windows
    # cap.release()
    # cv2.destroyAllWindows()

    return color, hsvValue, YUV_Value, [squareOffset, squareSize]
