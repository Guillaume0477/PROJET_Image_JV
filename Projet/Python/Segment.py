import numpy as np
import cv2

def getHSVColorSeg(im, bounds, refColor, toleranceH = 10):
    # toleranceH = 10
    toleranceS = 60
    toleranceV = 100

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


def getnorm(ref, current, w):
    frame_norm = w[0]*(current[:,:,0]-ref[0])**2 + w[1]*(current[:,:,1]-ref[1])**2 + w[2]*(current[:,:,2]-ref[2])**2 + w[3]*(current[:,:,3]-ref[3])**2 + w[4]*(current[:,:,4]-ref[4])**2 + w[5]*(current[:,:,5]-ref[5])**2
    return frame_norm


def getnorm_ND(ref, current, w, N):
    frame_norm = np.float64( current[:,:,0]*0 )
    print("taill frame_norm test ",np.shape(frame_norm))

    for ind in range (N):
        frame_norm += w[ind]*(current[:,:,ind]-ref[ind])**2 
    return frame_norm



def getnorm_1D(ref, current, w, ind):
    frame_norm = w[ind]*(current[:,:,ind]-ref[ind])**2 
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

    seuil = 30

    w=np.array([0.1,0.05,0.05,0.55,0.2,0.05])

    # print(type(refColorBGR))
    # print(refColorBGR)
    # print(type(refColorHSV))
    # print(refColorHSV)


    refcolor=np.concatenate([refColorBGR,refColorHSV],0)
    # print(refcolor)

    #Extraction de la zone d'intérêt
    frame = im[bounds[0]:bounds[1], bounds[2]:bounds[3],:] #im;
    #Passage en HSV
    hsvIm = cv2.cvtColor(im[bounds[0]:bounds[1],bounds[2]:bounds[3],:], cv2.COLOR_BGR2HSV)
    #hsvIm = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)


    current=np.concatenate([frame,hsvIm],2)
    # print(np.shape(current))


    frame_norm = getnorm(refcolor,current,w)
    # print(np.shape(frame_norm))

    #segR = cv2.equalizeHist(np.uint8(np.sqrt( getnorm(refcolor,current,w))))
    segR = np.sqrt( getnorm(refcolor,current,w))

    # print("MEAN", np.mean(np.mean(segR)))
    # print("MAX", np.max(np.max(segR)))


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





def getHSVBGRYUVColorSeg(im, bounds, refColorBGR, refColorHSV, YUV_Value):

    seuil = 15

    w=np.array([0.1,0.05,0.05,0.55,0.2,0.05,0,0,0])


    # print(type(refColorBGR))
    # print(refColorBGR)
    # print(type(refColorHSV))
    # print(refColorHSV)


    refcolor=np.concatenate((np.concatenate([refColorBGR,refColorHSV],0),YUV_Value),0)
    print(refcolor)


    #Extraction de la zone d'intérêt
    frame = im[bounds[0]:bounds[1], bounds[2]:bounds[3],:] #im;
    #Passage en HSV
    hsvIm = cv2.cvtColor(im[bounds[0]:bounds[1],bounds[2]:bounds[3],:], cv2.COLOR_BGR2HSV)
    #hsvIm = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

    #Passage en YUV
    img_to_yuv = cv2.cvtColor(im[bounds[0]:bounds[1],bounds[2]:bounds[3],:], cv2.COLOR_BGR2YUV)


    #np.concatenate([frame,hsvIm],2)
    current=np.concatenate((np.concatenate([frame,hsvIm],2),img_to_yuv),2)

    frame_norm = getnorm_ND(refcolor,current,w,9)


    #segR = cv2.equalizeHist(np.uint8(np.sqrt( getnorm(refcolor,current,w))))
    segR = np.sqrt( frame_norm)

    # print("MEAN", np.mean(np.mean(segR)))
    # print("MAX", np.max(np.max(segR)))


    #segR = np.array(cv2.inRange(segR, 0, seuil))


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
    Y=cv2.equalizeHist(np.uint8(np.sqrt(getnorm_1D(refcolor,current,w,6))))
    U=cv2.equalizeHist(np.uint8(np.sqrt(getnorm_1D(refcolor,current,w,7))))
    V2=cv2.equalizeHist(np.uint8(np.sqrt(getnorm_1D(refcolor,current,w,8))))
    
    

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

    return segR, B, G, R, S, H, V, Y ,U ,V2



