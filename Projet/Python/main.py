import Calibrage
import Track
import DetectParams
import Segment
import Py_utils as utils
import cv2
import matplotlib.pyplot as plt
import numpy as np
from math import floor
import os
from datetime import datetime
import pickle
import socket

def init_connexion_Unity():
    
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5065

    return (socket.socket(socket.AF_INET, socket.SOCK_DGRAM),UDP_IP,UDP_PORT)

def handle_pile(sock,UDP_IP,UDP_PORT,Pile,index,current_signe):

    Pile[index] +=1
    if (Pile[index] == 10):
        print("inhandle")
        Pile[0] = 0
        Pile[1] = 0
        Pile[2] = 0
        Pile[3] = 0
        Pile[4] = 0
        #current_signe = index
        print("current_signe",current_signe)
        print("index",index)

        #if not (current_signe==0): #si on est en possition neutre sinon on ne peux pas chager de signe
        if (current_signe==0):
            if index==0:
                return False
            else:
                sock.sendto( ("Signe_"+str(index)+"!").encode(), (UDP_IP, UDP_PORT) )
                print("_"*10, "Signe_"+str(index)+"!", "_"*10)
                current_signe = index
                return True
        else:
            if index != 0 :
                return False
            else:
                sock.sendto( ("Signe_"+str(index)+"!").encode(), (UDP_IP, UDP_PORT) )
                print("_"*10, "Signe_"+str(index)+"!", "_"*10)
                current_signe = index
                return True

            
            
        #      and index==0: #avant non 0 puis 0
        #     sock.sendto( ("Signe_"+str(index)+"!").encode(), (UDP_IP, UDP_PORT) )
        #     print("_"*10, "Signe_"+str(index)+"!", "_"*10)
        #     current_signe = index

        # elif (index==current_signe): #boucle en autre signe annulé
        #     print("idem")

        # elif (index==0) and (current_signe==0): #boucle en 0
        #     sock.sendto( ("Signe_"+str(index)+"!").encode(), (UDP_IP, UDP_PORT) )
        #     print("_"*10, "Signe_"+str(index)+"!", "_"*10)

        # elif ((not (index==0)) and (current_signe==0)): #de 0 à autre signe
        #     sock.sendto( ("Signe_"+str(index)+"!").encode(), (UDP_IP, UDP_PORT) )
        #     print("_"*10, "Signe_"+str(index)+"!", "_"*10)

        
        print("current_signe2",current_signe)
        return True
    return False




def handle_sending_Unity(sock,UDP_IP,UDP_PORT,svm_result,Pile,current_signe):
    if (svm_result == 0):
        if (handle_pile(sock,UDP_IP,UDP_PORT,Pile,0,current_signe)):
            current_signe=0
    if (svm_result == 1):
        if handle_pile(sock,UDP_IP,UDP_PORT,Pile,1,current_signe):
            current_signe=1
    if (svm_result == 2):
        if handle_pile(sock,UDP_IP,UDP_PORT,Pile,2,current_signe):
            current_signe=2
    if (svm_result == 3):
        if handle_pile(sock,UDP_IP,UDP_PORT,Pile,3,current_signe):
            current_signe=3
    if (svm_result == 4):
        if handle_pile(sock,UDP_IP,UDP_PORT,Pile,4,current_signe):
            current_signe=4
    return current_signe

def main():

    sock,UDP_IP,UDP_PORT = init_connexion_Unity()

    nombre_signes=5
    current_signe= 0

    Pile=[0]*nombre_signes




    #Config cam
    cap = cv2.VideoCapture(0)
    play = True

    #Hand calibration
    colorHand, hueValue, YUV_Value, [squareOffset, squareSize] = Calibrage.HandCalibrate(cap)
    found = True

    filename = "svmModel.pkl"
    with open(filename, 'rb') as file:
        svm = pickle.load(file)

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
        # segR = Segment.getHSVColorSeg(frame, bounds, hueValue)
        #segR = Segment.getBGRColorSeg(frame, bounds, colorHand)

        segR, B, G, R, S, H, V = Segment.getHSVBGRColorSeg(frame, bounds, colorHand, hueValue)

        # segR, B, G, R, S, H, V, Y, U, V2 = Segment.getHSVBGRYUVColorSeg(frame, bounds, colorHand, hueValue, YUV_Value)

        # # Cleaning of the space to better segment hand
        segR = utils.Cleaning(segR)

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
            #print(svm.predict(Params))

            current_signe = handle_sending_Unity(sock,UDP_IP,UDP_PORT,svm.predict(Params),Pile,current_signe)

            # # #Display gravity center on screen
            # segR[int(Params[0][3]*segR.shape[0]), :] = 127
            # segR[:, int(Params[0][4]*segR.shape[1])] = 127

            # # Tests to update hsv channel while playing to be adaptative
            # hueValue = utils.UpdateColor(segR, frame[xmin:xmax, ymin:ymax, :])
            pass
        
        # Display the segmentation on screen 
        frame[xmin:xmax,ymin:ymax,0] = segR
        frame[xmin:xmax,ymin:ymax,1] = segR
        frame[xmin:xmax,ymin:ymax,2] = segR
        # frame[:,:,0] = segR
        # frame[:,:,1] = segR
        # frame[:,:,2] = segR
        
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
        
        #Acquire new data
        if key == ord('@'):
            #Label of the position recorded (if several to be labeled later, set -1)
            label = 3
            #Path to write images
            pathToWrite = "TrainImagesULT2"
            #Current date and time
            d = datetime.now()

            #Check if path already exists
            if not os.path.exists(pathToWrite):
                os.mkdir(pathToWrite)
            #Write segmentation as an image
            strUlt = os.path.join(pathToWrite , "imTest_" + str(d.date()) + '_' + str(d.time())[3:5] + '_' + str(d.time())[6:8] + "_" + str(label) +".png")
            print(strUlt)
            cv2.imwrite(strUlt, segR)

        #Show the frame
        cv2.imshow('Capture Video', frame)
        # cv2.imshow('B', B)
        # cv2.imshow('G', G)
        # cv2.imshow('R', R)
        # cv2.imshow('H', H)
        # cv2.imshow('S', S)
        # cv2.imshow('V', V)
        # cv2.imshow('Y', Y)
        # cv2.imshow('U', U)
        # cv2.imshow('V2', V2)



        

        

    #Destroy windows
    cap.release()
    cv2.destroyAllWindows()
    return 0


main()