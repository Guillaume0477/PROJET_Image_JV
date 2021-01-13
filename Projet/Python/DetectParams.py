import numpy as np
import cv2

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

    grad = GetGradient(seg)
    if np.sum(grad) != 0 :
        getConvexEnvelop(grad)
    
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
    im = (im+np.min(im))/(np.max(im)+np.min(im)+0.00001)*255

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
    #Indexes vers gradient is nonzero
    ids = np.argwhere(gradIm > 0)
    #minimum x value
    xmin = np.argwhere(np.min(ids[:,0]) == ids[:,0])
    #Initialization of the lists of the points of the convex envelop
    listPoints = [ids[xmin[0][0],:]]

    while True:

        cosmax = 0

        #Check si la liste ne contient qu'un point et considère le point précédent
        if len(listPoints) <= 1:
            former = np.copy(ids[xmin[0][0],:])
            former[1] -= 1
        else :
            former = listPoints[-2]

        #Récupère le point actuel
        current = listPoints[-1]

        #Normalisation des vecteurs
        v1 = (former - current)/np.linalg.norm(former-current)
        v2s = (ids - current)

        v2sN = np.reshape(np.sqrt(np.sum(np.square(v2s), axis = 1)), [v2s.shape[0],1])+0.00001

        v2s = np.divide(v2s,v2sN)

        #Calcul du cos
        coss = np.dot(v2s,v1)
        coss[xmin] = 1

        #Conservation du cos minimum
        xmin = np.argwhere(coss == np.min(coss))[0][0]
        listPoints.append(ids[xmin,:])

        if np.linalg.norm(listPoints[0] - listPoints[-1]) == 0:
            break


    # p0 = listPoints[0]
    # for point in listPoints[1:]:
    #     cv2.line(gradIm, tuple(np.flip(p0)), tuple(np.flip(point)), (127), thickness=8)
    #     p0 = point

    # cv2.imshow('im',gradIm)

    return 0

def getNbFing(listPts):

    

    return 0