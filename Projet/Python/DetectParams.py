import numpy as np

def getParameters(im, seg):
    #List of relevant parameters
    paramsSet = []
    
    #Include bounding box size and covered area
    paramsSet = [np.shape(seg), np.sum(seg)]

    #Get gravity center
    Gcenter = getGravityCenter(seg)
    #Include gravity center
    paramsSet.append(Gcenter)
    #Include maximum signed distance
    paramsSet.append(getSignedDistance(seg,Gcenter))

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