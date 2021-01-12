import numpy as np

def getParameters(im, seg):

    paramsSet = []
    
    paramsSet = [np.shape(seg), np.sum(seg)]

    Gcenter = getGravityCenter(seg)

    paramsSet.append(Gcenter)


    paramsSet.append(getSignedDistance(seg,Gcenter))

    return paramsSet

def getGravityCenter(seg):

    Sx = np.sum(seg, axis = 1)
    Sy = np.sum(seg, axis = 0)

    Sx = Sx / np.max(Sx)
    Sy = Sy / np.max(Sy)


    idx = np.argwhere(Sx)
    idy = np.argwhere(Sy)

    centerx = np.sum(idx*Sx[idx]) / np.sum(Sx[idx])
    centery = np.sum(idy*Sy[idy]) / np.sum(Sy[idy])

    return [centerx, centery]
    
def getSignedDistance(seg, G):

    d = [0,0]

    sx = np.nonzero(np.sum(seg, 0))
    sy = np.nonzero(np.sum(seg, 1))

    xmin, xmax = sx[0][0], sx[0][-1]
    ymin, ymax = sy[0][0], sy[0][-1]
    
    Gx = [G[0] - xmin, G[0] - xmax]
    Gy = [G[1] - ymin, G[1] - ymax]
    print(G)
    print(Gx, Gy)
    distx = np.max(np.abs(Gx))
    disty = np.max(np.abs(Gy))

    if distx == abs(Gx[0]): d[0] = Gx[0] 
    else : d[0] = Gx[1]

    if disty == abs(Gy[0]) : d[1] = Gy[1]
    else : d[1] = Gy[1] 

    print(d)
    return d 
