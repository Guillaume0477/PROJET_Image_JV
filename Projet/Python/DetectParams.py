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