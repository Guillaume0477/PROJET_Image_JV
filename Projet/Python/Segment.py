import numpy as np
import cv2

def getSegmentation(im, bounds, BGRColor, HSVColor):

    segR = np.zeros(bounds[1]-bounds[0], bounds[3] - bounds[2])






    return segR

def getHSVColorSeg(im, bounds, refColor):
    toleranceH = 10
    toleranceS = 60
    toleranceV = 60

    #Passage en HSV
    hsvIm = cv2.cvtColor(im[bounds[0]:bounds[1],bounds[2]:bounds[3],:], cv2.COLOR_BGR2HSV)

    #Segmentation sur la teinte
    segR = np.array(cv2.inRange(hsvIm[:,:,0], refColor[0]-toleranceH, refColor[0]+toleranceH))/255
    #Segmentation sur la saturation
    segR *= np.array(cv2.inRange(hsvIm[:,:,1], refColor[1]-toleranceS, refColor[1]+toleranceS))/255
    #Segmentation sur la value
    segR *= np.array(cv2.inRange(hsvIm[:,:,2], refColor[2]-toleranceV, refColor[2]+toleranceV))/255
    segR = np.uint8(segR*255)

    return segR


def getBGRColorSeg(im, bounds, refColor):
    tolerance = 30

    #Extraction de la zone d'intérêt
    frame = im[bounds[0]:bounds[1], bounds[2]:bounds[3],:]

    #Segmentation sur chaque canal
    segR = np.array(cv2.inRange(frame, refColor[0]-tolerance, refColor[0]+tolerance))
    segR *= np.array(cv2.inRange(frame, refColor[1]-tolerance, refColor[1]+tolerance))
    segR *= np.array(cv2.inRange(frame, refColor[2]-tolerance, refColor[2]+tolerance))
    
    return segR

def GetGradient(BWim):
    SobelHcontours = np.array([[-1,-1,-1], [0,0,0], [1,1,1]])
    SobelVcontours = np.array([[-1,0,1], [-1,0,1], [-1,0,1]])

    gradH = cv2.filter2D(BWim, -1, SobelHcontours)
    gradV = cv2.filter2D(BWim, -1, SobelVcontours)

    # cv2.imshow('H',gradH)
    # cv2.imshow('V', gradV)

    gauss = cv2.GaussianBlur(BWim, (5, 5), 2)

    # cv2.imshow('gauss', gauss)


    return 0
    