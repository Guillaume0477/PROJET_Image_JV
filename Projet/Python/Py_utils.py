import cv2
import numpy as np

def Cleaning(im):
    
    #Closing
    structElemEro = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    structElemDil = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    im = cv2.erode(im, structElemEro)
    im = cv2.dilate(im, structElemDil)

    #Median filter
    ksize = 9
    kernel = np.ones([ksize, ksize])
    im = cv2.medianBlur(im, ksize)

    return im

def UpdateColor(seg, im):


    test = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

    print(test[0,0,:])
    print(im[0,0,:])

    S = np.tile(seg, [3,1,1])
    S = np.swapaxes(S,0,2)
    S = np.swapaxes(S,0,1)
    S = (S/255)
    I = np.uint8(im*S)

    s = 255*np.sum(np.sum(I, axis = 0), axis = 0) / np.sum(seg)

    print(s)

    cv2.imshow("pilou", I)

    return s
