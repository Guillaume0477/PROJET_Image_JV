import cv2
import numpy as np
from math import floor

def HandCalibrate(cap):

    print("Put your hand inside the square and push 'G'")

    acq = True

    squareSize = [100,100]
    squareOffset = [200,200]

    color = [0,0,0]

    while acq :
        #Get the frame
        ret,frame = cap.read()

        #Detect user quit command
        key = cv2.waitKey(1)
        
        if key == ord('g'):

            ymin = floor(squareOffset[1] + squareSize[1]/3)
            ymax = floor(squareOffset[1] + 2*squareSize[1]/3)
            xmin = floor(squareOffset[0] + 4*squareSize[0]/7)
            xmax = floor(squareOffset[0] + 6*squareSize[0]/7)
            color = np.mean(np.mean(frame[xmin:xmax, ymin:ymax,:], axis = 0),axis = 0)

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
        #Increase square size
        elif key == ord('a'):
            squareSize[0] = max(100, squareSize[0]-20)
            if(squareSize[0] != squareSize[1]):
                squareSize[1] = squareSize[0]
                squareOffset[1] = min(squareOffset[1]+10, np.shape(frame)[1]-1-squareSize[1])
                squareOffset[0] = min(squareOffset[0]+10, np.shape(frame)[0]-1-squareSize[0])
        #Reduce square size
        elif key == ord('e'):
            squareSize[0] = np.min([squareSize[0]+20, np.shape(frame)[0]-1, squareSize[1]+20, np.shape(frame)[1]-1])
            if(squareSize[0] != squareSize[1]):
                squareSize[1] = squareSize[0]
                squareOffset[1] = max(0, squareOffset[1]-10)
                squareOffset[0] = max(0,squareOffset[0]-10)     

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
    print(color)
    return color, [squareOffset, squareSize]
