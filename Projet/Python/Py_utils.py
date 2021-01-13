import cv2
import numpy as np
from math import floor, sqrt, pi
import matplotlib.pyplot as plt


def getGaussianKernel(sx, sy, mu = 0, sigma = 50):
    #Creation of meshgrids along x and y
    Y = np.linspace(-floor(sy/2), floor((sy-1)/2), sy)*np.ones([sx,sy])
    X = np.linspace(-floor(sx/2), floor((sx-1)/2), sx)*np.ones([sy,sx])
    X = np.transpose(X)

    #Creation of a gaussian kernel
    S = 1.0/sqrt(2*pi*sigma) * (np.exp(-(np.square(X)+np.square(Y))/(2*sigma*sigma)))

    return S
    

def Cleaning(im):
    
    #Structuring elements for erosion
    structElemEro = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    #Structuring element for dilation
    structElemDil = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    
    # # Erosion
    # im = cv2.erode(im, structElemEro)

    # #Median filter
    ksize = 3
    im = cv2.medianBlur(im, ksize)

    # Dilation
    im = cv2.dilate(im, structElemDil)

    # # Gaussian filtering in Fourier space
    # G = getGaussianKernel(np.shape(im)[0], np.shape(im)[1])
    # IM = np.fft.fft2(im/255)
    # IM = np.fft.fftshift(IM)
    # newIm = np.abs(np.fft.ifft2(IM*G))*255
    # cv2.imshow('rec', newIm)
    # cv2.imshow('fft', G*np.abs(IM) / np.max(np.abs(IM)))


    return im



def UpdateColor(seg, im):

    # Convert to hsv
    hsvIm = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

    # Mask according to the segmentation the hand
    S = np.tile(seg, [3,1,1])
    S = np.swapaxes(S,0,2)
    S = np.swapaxes(S,0,1)
    S = (S/255)
    I = np.uint8(hsvIm*S)

    # Get the mean color
    s = np.sum(np.sum(I, axis = 0), axis = 0) / np.sum(seg)

    #Adapt hsv values
    s[0] *= 179
    s[1:3] *= 255

    # print(s)

    return s

