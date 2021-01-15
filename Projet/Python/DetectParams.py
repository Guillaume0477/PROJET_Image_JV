import numpy as np
import cv2
from math import sqrt, floor
import matplotlib.pyplot as plt
import time

def getParameters(im, seg):
    # List of relevant parameters
    paramsSet = np.zeros([1,15])

    # Include bounding box size and covered area
    shape = np.shape(seg)
    # paramsSet[:,0:2] = np.array(shape)[0:2]
    area = np.sum(seg)
    paramsSet[:,2] = area/(shape[0]*shape[1])/255

    # Get gravity center
    Gcenter = getGravityCenter(seg)
    # Include gravity center
    paramsSet[:,3:5] = [Gcenter[0]/shape[0], Gcenter[1]/shape[1]]

    #NOT RELEVANT
    # #Surface above and under the gravity center
    # ST = np.sum(seg[:floor(Gcenter[0]),:])/area
    # SB = np.sum(seg[floor(Gcenter[0]):,:])/area
    # print(SB, ST)

    # Include maximum signed distance
    SignDist = getSignedDistance(seg,Gcenter)
    paramsSet[:,5:7] = [SignDist[0]/shape[0], SignDist[1]/shape[1]]

    grad = GetGradient(seg)
    # ids = np.argwhere(grad > 0)
    if np.sum(grad) != 0 :
        listPts = np.array(getConvexEnvelop(grad))
        
        nbHT = np.sum(listPts[:,0] > Gcenter[0])
        nbHB = listPts.shape[0] - nbHT
        paramsSet[:,7] = nbHT
        paramsSet[:,8] = nbHB
        
        listPts = np.array(cleanConvex(listPts))
        nbHT = np.sum(listPts[:,0] > Gcenter[0])
        nbHB = listPts.shape[0] - nbHT
        paramsSet[:,9] = nbHT
        paramsSet[:,10] = nbHB
        
        #NOT RELEVANT
        # a = np.mean(np.linalg.norm(listPts[:-1] - listPts[1:], axis = 1))
        # print(a/(sqrt(seg.shape[0]*seg.shape[0] + seg.shape[1]*seg.shape[1])))
        #NOT REVLEVANT
        # sortGradPts(ids)

        #TO BE DISCUSSED
        # getNbFing(listPts, grad)
    
    vects = getPCADir(seg)    
    ProjCaract = getProjCaract(seg, vects)
    paramsSet[:,0:2] = ProjCaract[0:2]
    paramsSet[:,11:15] = ProjCaract[2:]

    # print(np.array(paramsSet)[:,7:])

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

        v2sN = np.reshape(np.linalg.norm(v2s, axis = 1), [v2s.shape[0], 1])
        v2s = np.divide(v2s,v2sN+0.00001)

        #Calcul du cos
        coss = np.dot(v2s,v1)
        coss[xmin] = 1

        #Conservation du cos minimum
        xmin = np.argwhere(coss == np.min(coss))[0][0]
        listPoints.append(ids[xmin,:])

        if np.linalg.norm(listPoints[0] - listPoints[-1]) == 0:
            break


    p0 = listPoints[0]
    for point in listPoints[1:]:
        cv2.line(gradIm, tuple(np.flip(p0)), tuple(np.flip(point)), (127), thickness=8)
        p0 = point

    cv2.imshow('im',gradIm)

    return listPoints

def getNbFing(listPts, gradIm):
    #Indexes vers gradient is nonzero
    ids = np.argwhere(gradIm > 0)
    
    p0 = listPts[0]

    listDefects = []

    for p in listPts[1:]:
        #Creation of the vector and its norm
        convexSeg = p-p0
        convN = np.linalg.norm(convexSeg)


        #Projection of contour points on the vector
        vects = ids - p0

        NVects = np.reshape(np.linalg.norm(vects, axis = 1), [vects.shape[0],1])
        NProj = np.reshape(np.dot(vects,convexSeg/(convN+0.0001)), [vects.shape[0],1])
        NDist = np.sqrt(np.square(NVects)-np.square(NProj))

        #Seperate the vector in subsegments
        numSub = 20            #Number of segments
        inc = convN / numSub    #Increments (size of the subsegment)
        maxi = 0                #Maximum distance
        index = [0,0]           #Point distance

        for k in range(numSub):

            #Indexes of the points inside the projection of which is located inside the segment
            a = np.argwhere(np.multiply((NProj > k*inc),(NProj <= (k+1)*inc)))
            if len(a) < 1 :
                continue
            a = a[:,0]
            # print('P', NProj[a], k*inc, (k+1)*inc)

            #Minimum value distance from the envelop to the contour inside the segment
            b = np.argwhere(np.min(NDist[a]) == NDist[a])[:,0]
        
            if (len(b) > 1) :
                b = b[0]

            #Get the distance
            d = NDist[a[b]]

            if d > maxi :
                maxi = d
                index = ids[a[b]]

        if (maxi != 0):
            listDefects.append(index)
        p0 = p

    # print(listPts, np.shape(listPts))
    # print(listDefects, np.shape(listDefects))
    
    p0 = listPts[0]
    for k in range(len(listDefects)) :
        i = tuple(np.flip(listDefects[k])[0])
        cv2.circle(gradIm, i, (20), (255,0,0))#, thickness=8)

    for point in listPts[1:] :
        cv2.line(gradIm, tuple(np.flip(p0)), tuple(np.flip(point)), (127), thickness=8)
        p0 = point

    cv2.imshow('defects', gradIm)

    # print()
    # print()
    return 0

def cleanConvex(listPts):
    listCleaned = [listPts[0]]

    for p in listPts[1:]:
        v = listCleaned[-1] - p
        if (np.linalg.norm(v) > 50):
            listCleaned.append(p)

    return listCleaned

def getProjCaract(seg, dir):
    sInit = seg.shape
    
    projx = np.sum(seg, axis = 0)
    projy = np.sum(seg, axis = 1)

    #Size of the true bounding box compared to the square box
    sx, sy = np.sum(projx != 0)/projx.shape[0], np.sum(projy != 0)/projy.shape[0]

    #Mean value and standard Deviations
    argx = np.argwhere(projx>0)
    argy = np.argwhere(projy>0)
    mux = np.sum(projx[argx]*argx)/np.sum(projx[argx])/sInit[0]
    muy = np.sum(projy[argy]*argy)/np.sum(projy[argy])/sInit[1]

    h0, h1 = getProjection(seg, dir)

    plt.figure(0)
    # plt.plot(h0)
    plt.plot(h1)


    maxix = np.argwhere(h1 == np.max(h1))[0][0]
    
    maxiVal = h1[maxix]
    thresh = 3.0/4.0*maxiVal

    PT = 1.0*(h1 > thresh)
    plt.plot(PT*maxiVal)
    plt.plot(np.gradient(PT)*maxiVal)
    # plt.show()

    G = np.gradient(PT)[range(0,PT.shape[0], 2)]
    
    nbMaxis = np.sum(G == 0.5)

    numP = np.argwhere(G > 0)
    numN = np.argwhere(G < 0)

    

    sizeInt = (numN - numP)[:,0]

    nbMaxis -= np.sum(sizeInt < 5)

    maxix /= sInit[0]


    # print(nbMaxis)
    # print(nbMaxis)
    # plt.figure(0)
    # plt.plot(projx)
    # plt.plot(projy)
    # plt.plot(PT)
    # plt.plot(G*maxiVal)
    # plt.show()
    
    # print(sx, sy)

    return [sx, sy, mux, muy, maxix, nbMaxis]


def getProjection(seg, dir):
    ids = np.argwhere(seg)
    segS = seg.shape

    coss0 = np.floor(np.dot(ids, dir[0,:]))
    coss1 = np.floor(np.dot(ids, dir[1,:]))

    h0 = np.histogram(coss0, bins = floor(np.max(coss0)-np.min(coss0)))
    h1 = np.histogram(coss1, bins = floor(np.max(coss1)-np.min(coss1)))

    # plt.figure(0)
    # plt.plot(h0[1][:-1], h0[0])
    # plt.plot(h1[1][:-1], h1[0])
    # plt.show()
    # h1 = np.histogram(coss1, bin = [])

    # print(coss0, coss1)
    return h0[0], h1[0]


######################################
# NOT RELEVANT : TOO LONG TO COMPUTE #
######################################
def sortGradPts(listPts):

    for k in range(len(listPts)-1):
        #Point to compare
        p = listPts[k]

        #Norm of the vectors from p
        L = np.linalg.norm(listPts[k+1:]-p, axis = 1)
        
        # print(L)
        # print(p)
        # exit()
        #Index of the closer point(s)
        i = np.argwhere(L == np.min(L))[0][0]

        #Swap points
        mem = np.copy(listPts[k+1])
        listPts[k+1] = np.copy(listPts[k+1+i])
        listPts[i+k+1] = mem
        

    # print(listPts[0], listPts[-1])

def getPCADir(seg):
    ids = np.argwhere(seg)
    mu = np.mean(ids, 0)

    idsC = ids - mu
    Px = np.matmul(np.transpose(idsC), (idsC))

    lambd, vect = np.linalg.eig(Px)


    cv2.line(seg, tuple([floor(seg.shape[0]/2), floor(seg.shape[1]/2)]), tuple([floor(seg.shape[0]/2 + 50*vect[0,0]), floor(seg.shape[1]/2 + 50*vect[0,1])]), 0)
    cv2.line(seg, tuple([floor(seg.shape[0]/2), floor(seg.shape[1]/2)]), tuple([floor(seg.shape[0]/2 + 50*vect[1,0]), floor(seg.shape[1]/2 + 50*vect[1,1])]), 0)

    cv2.imshow('.', seg)
    # plt.figure(0)
    # plt.plot([1,1])
    # plt.show()
    return vect

