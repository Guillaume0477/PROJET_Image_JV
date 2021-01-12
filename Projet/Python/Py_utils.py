import cv2
import numpy as np

from math import floor, sqrt, pi
import matplotlib.pyplot as plt


def getGaussianKernel(sx, sy, mu = 0, sigma = 50):
    Y = np.linspace(-floor(sy/2), floor((sy-1)/2), sy)*np.ones([sx,sy])
    X = np.linspace(-floor(sx/2), floor((sx-1)/2), sx)*np.ones([sy,sx])
    X = np.transpose(X)

    S = 1.0/sqrt(2*pi*sigma) * (np.exp(-(np.square(X)+np.square(Y))/(2*sigma*sigma)))

    return S
    

def Cleaning(im):
    
    #Closing
    structElemEro = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    structElemDil = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    # im = cv2.erode(im, structElemEro)

    # #Median filter
    ksize = 9

    kernel = np.ones([ksize, ksize])
    im = cv2.medianBlur(im, ksize)


    im = cv2.dilate(im, structElemDil)



    # G = getGaussianKernel(np.shape(im)[0], np.shape(im)[1])
    # IM = np.fft.fft2(im/255)
    # IM = np.fft.fftshift(IM)

    # newIm = np.abs(np.fft.ifft2(IM*G))*255

    # cv2.imshow('rec', newIm)
    # cv2.imshow('fft', G*np.abs(IM) / np.max(np.abs(IM)))


    return im



def UpdateColor(seg, im):

    hsvIm = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

    S = np.tile(seg, [3,1,1])
    S = np.swapaxes(S,0,2)
    S = np.swapaxes(S,0,1)
    S = (S/255)

    I = np.uint8(hsvIm*S)

    s = np.sum(np.sum(I, axis = 0), axis = 0) / np.sum(seg)

    s[0] *= 179
    s[1:3] *= 255

    # print(s)

    return s

