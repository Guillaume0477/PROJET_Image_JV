import numpy as np

def getParameters(im, seg):
    # List of relevant parameters
    paramsSet = np.zeros([1,7])

    # Include bounding box size and covered area
    shape = np.shape(seg)
    paramsSet[:,0:2] = np.array(shape)[0:2]
    paramsSet[:,2] = np.sum(seg)/(shape[0]*shape[1])/255

    # Get gravity center
    Gcenter = getGravityCenter(seg)
    # Include gravity center
    paramsSet[:,3:5] = [Gcenter[0]/shape[0], Gcenter[1]/shape[1]]

    # Include maximum signed distance
    SignDist = getSignedDistance(seg,Gcenter)
    paramsSet[:,5:7] = [SignDist[0]/shape[0], SignDist[1]/shape[1]]
    
    return paramsSet

def getGravityCenter(seg):
    # Sum of the square along x and y axis
    Sx = np.sum(seg, axis = 1)
    Sy = np.sum(seg, axis = 0)
    # Normalization
    Sx = Sx / np.max(Sx)
    Sy = Sy / np.max(Sy)
    # Get indexes with non zeros
    idx = np.argwhere(Sx)
    idy = np.argwhere(Sy)
    # Get gravity center
    centerx = np.sum(idx*Sx[idx]) / np.sum(Sx[idx])
    centery = np.sum(idy*Sy[idy]) / np.sum(Sy[idy])

    return [centerx, centery]
    
def getSignedDistance(seg, G):
    d = [0,0]

    # Sum of the square along x and y axis
    sx = np.nonzero(np.sum(seg, 0))
    sy = np.nonzero(np.sum(seg, 1))

    #Get the furthest indexes
    xmin, xmax = sx[0][0], sx[0][-1]
    ymin, ymax = sy[0][0], sy[0][-1]

    #Caculate the distance between the extremes and the gravity center
    Gx = [G[0] - xmin, G[0] - xmax]
    Gy = [G[1] - ymin, G[1] - ymax]

    #Maximum distance
    distx = np.max(np.abs(Gx))
    disty = np.max(np.abs(Gy))

    #Update the sined distance
    if distx == abs(Gx[0]): d[0] = Gx[0]
    else : d[0] = Gx[1]

    if disty == abs(Gy[0]) : d[1] = Gy[1]
    else : d[1] = Gy[1]

    return d


def GetGradient(BWim):
    # Gradient à partir des filtres de Sobel
    SobelHcontours = np.array([[-1,-1,-1], [0,0,0], [1,1,1]])
    SobelVcontours = np.array([[-1,0,1], [-1,0,1], [-1,0,1]])

    #Segmentation des contours horizontaux
    gradH = cv2.filter2D(np.int16(BWim/255), -1, SobelHcontours)
    #Segmentation des contours verticaux
    gradV = cv2.filter2D(np.int16(BWim/255), -1, SobelVcontours)
    #Norme du gradient
    im = (gradH*gradH + gradV*gradV)
    im = (im+np.min(im))/(np.max(im)+np.min(im))*255

    # cv2.imshow("extr", im)
    # cv2.imshow('H',np.abs(gradH)/np.max(np.abs(gradV))*255)
    # cv2.imshow('V', np.abs(gradV)/np.max(np.abs(gradV))*255)


    # # Utilisation de gaussienne pour filtre passe bas
    # gauss = cv2.GaussianBlur(BWim, (5, 5), 2)

    # cv2.imshow('gauss', gauss)

    # # Test pour la détection du bout des doigts
    # test = np.array([[0,1,0], [1,1,1], [1,1,1]])
    # extr = cv2.filter2D(np.array(BWim/255), -1, test)

    return im

def getConvexEnvelop(gradIm):

    ids = np.argwhere(gradIm > 0)



    return 0
