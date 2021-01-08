import numpy as np

def getParameters(im, seg):

    paramsSet = []
    
    paramsSet = [np.shape(seg), np.sum(seg)]

    Gcenter = getGravityCenter(seg)

    paramsSet.append(Gcenter)

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
    