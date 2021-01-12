import numpy as np
import cv2

def getHSVColorSeg(im, bounds, refColor, toleranceH = 15):
    # toleranceH = 10
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
    tolerance = 60

    #Extraction de la zone d'intérêt
    frame = im[bounds[0]:bounds[1], bounds[2]:bounds[3],:]

    #Segmentation sur chaque canal
    segR = np.array(cv2.inRange(frame[:,:,0], refColor[0]-tolerance, refColor[0]+tolerance))
    segR *= np.array(cv2.inRange(frame[:,:,1], refColor[1]-tolerance, refColor[1]+tolerance))
    segR *= np.array(cv2.inRange(frame[:,:,2], refColor[2]-tolerance, refColor[2]+tolerance))
    
    return segR


def getnorm(ref, current, w):
    frame_norm = w[0]*(current[:,:,0]-ref[0])**2 + w[1]*(current[:,:,1]-ref[1])**2 + w[2]*(current[:,:,2]-ref[2])**2 + w[3]*(current[:,:,3]-ref[3])**2 + w[4]*(current[:,:,4]-ref[4])**2 + w[5]*(current[:,:,5]-ref[5])**2
    return frame_norm

def getnorm_5(ref, current, w):
    frame_norm = w[5]*(current[:,:,5]-ref[5])**2
    return frame_norm


def getnorm_4(ref, current, w):
    frame_norm = w[4]*(current[:,:,4]-ref[4])**2
    return frame_norm


def getnorm_3(ref, current, w):
    frame_norm = w[3]*(current[:,:,3]-ref[3])**2
    return frame_norm


def getnorm_2(ref, current, w):
    frame_norm = w[2]*(current[:,:,2]-ref[2])**2
    return frame_norm


def getnorm_1(ref, current, w):
    frame_norm = w[1]*(current[:,:,1]-ref[1])**2 
    return frame_norm


def getnorm_0(ref, current, w):
    frame_norm = w[0]*(current[:,:,0]-ref[0])**2 
    return frame_norm


def getHSRBGRColorSeg(im, bounds, refColorBGR, refColorHSV):

    seuil = 70

    w=np.array([0.2,0.05,0.05,0.6,0.25,0.05])

    print(type(refColorBGR))
    print(refColorBGR)
    print(type(refColorHSV))
    print(refColorHSV)


    refcolor=np.concatenate([refColorBGR,refColorHSV],0)
    print(refcolor)

    #Extraction de la zone d'intérêt
    frame = im[bounds[0]:bounds[1], bounds[2]:bounds[3],:] #im;
    #Passage en HSV
    hsvIm = cv2.cvtColor(im[bounds[0]:bounds[1],bounds[2]:bounds[3],:], cv2.COLOR_BGR2HSV)
    #hsvIm = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)


    current=np.concatenate([frame,hsvIm],2)
    print(np.shape(current))


    frame_norm = getnorm(refcolor,current,w)
    print(np.shape(frame_norm))

    #segR = cv2.equalizeHist(np.uint8(np.sqrt( getnorm(refcolor,current,w))))
    segR = np.sqrt( getnorm(refcolor,current,w))

    print("MEAN", np.mean(np.mean(segR)))
    print("MAX", np.max(np.max(segR)))


    segR = np.array(cv2.inRange(segR, 0, seuil))


# import cv2 import 
# numpy img = cv2.imread ('pout.jpg') 
# img_to_yuv = cv2.cvtColor (img, cv2.COLOR_BGR2YUV) 
# img_to_yuv = cv2.cvtColor (img, cv2.COLOR_BGR2YUV) 
# img_to_yuv = cv2.cvtColor (img, cv2.COLOR_BGR2YUV) 
# img_to_yuv [:,:,0] = cv2.equalizeHist (img_to_yuv [:,:: 0])
# hist_equalization_result = cv2.cvtColor (img_to_yuv, cv2.COLOR_YUV2BGR) 
# cv2.imwrite ('result.jpg', hist_equalization_result)

    # B=np.sqrt(getnorm_0(refcolor,current,w))
    # G=np.sqrt(getnorm_1(refcolor,current,w))
    # R=np.sqrt(getnorm_2(refcolor,current,w))
    # H=np.sqrt(getnorm_3(refcolor,current,w))
    # S=np.sqrt(getnorm_4(refcolor,current,w))
    # V=np.sqrt(getnorm_5(refcolor,current,w))


    B=cv2.equalizeHist(np.uint8(np.sqrt(getnorm_0(refcolor,current,w))))
    G=cv2.equalizeHist(np.uint8(np.sqrt(getnorm_1(refcolor,current,w))))
    R=cv2.equalizeHist(np.uint8(np.sqrt(getnorm_2(refcolor,current,w))))
    H=cv2.equalizeHist(np.uint8(np.sqrt(getnorm_3(refcolor,current,w))))
    S=cv2.equalizeHist(np.uint8(np.sqrt(getnorm_4(refcolor,current,w))))
    V=cv2.equalizeHist(np.uint8(np.sqrt(getnorm_5(refcolor,current,w))))
    

    # current_color = np.concatenate



    # toleranceH = 15
    # toleranceS = 100
    # toleranceV = 60
    # tolerance = 15




    # #Segmentation sur chaque canal
    # segR = np.array(cv2.inRange(frame[:,:,0], refColorBGR[0]-tolerance, refColorBGR[0]+tolerance))
    # segR *= np.array(cv2.inRange(frame[:,:,1], refColorBGR[1]-tolerance, refColorBGR[1]+tolerance))
    # segR *= np.array(cv2.inRange(frame[:,:,2], refColorBGR[2]-tolerance, refColorBGR[2]+tolerance))
    


    # #Segmentation sur la teinte
    # segR *= np.array(cv2.inRange(hsvIm[:,:,0], refColorHSV[0]-toleranceH, refColorHSV[0]+toleranceH))/255
    # #Segmentation sur la saturation
    # segR *= np.array(cv2.inRange(hsvIm[:,:,1], refColorHSV[1]-toleranceS, refColorHSV[1]+toleranceS))/255
    # #Segmentation sur la value
    # segR *= np.array(cv2.inRange(hsvIm[:,:,2], refColorHSV[2]-toleranceV, refColorHSV[2]+toleranceV))/255
    # segR = np.uint8(segR*255)

    return segR, B, G, R, S, H, V





def GetGradient(BWim):
    # Gradient à partir des filtres de Sobel
    SobelHcontours = np.array([[-1,-1,-1], [0,0,0], [1,1,1]])
    SobelVcontours = np.array([[-1,0,1], [-1,0,1], [-1,0,1]])

    #Segmentation des contours horizontaux
    gradH = cv2.filter2D(BWim, -1, SobelHcontours)
    #Segmentation des contours verticaux
    gradV = cv2.filter2D(BWim, -1, SobelVcontours)

    # cv2.imshow('H',gradH)
    # cv2.imshow('V', gradV)

    # # Utilisation de gaussienne pour filtre passe bas
    # gauss = cv2.GaussianBlur(BWim, (5, 5), 2)

    # cv2.imshow('gauss', gauss)


    return 0
    
