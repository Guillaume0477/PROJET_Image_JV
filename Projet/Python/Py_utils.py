import cv2
import numpy as np

def Cleaning(im):
    
    structElemEro = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    structElemDil = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))

    im = cv2.erode(im, structElemEro)
    im = cv2.dilate(im, structElemDil)

    return im

def UpdateColor(seg, im):

    S = np.tile(seg, [3,1,1])
    S = np.swapaxes(S,0,2)
    S = np.swapaxes(S,0,1)
    S = (S/255)
    I = np.uint8(im*S)



    cv2.imshow("pilou", I)

    return [0,0,0]
