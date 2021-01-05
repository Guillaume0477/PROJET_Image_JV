import numpy as np

def trackHand(im, squareOffset, squareSize, fullSize):

    moveInc = 20
    sizeInc = 20

    im = np.array(im)
    s = np.shape(im)
    xmin = squareOffset[0]
    xmax = squareOffset[0] + squareSize[0]
    ymin = squareOffset[1]
    ymax = squareOffset[1] +  squareSize[1]

    sumLines = np.array([np.sum(im[0,:]), np.sum(im[s[0]-1,:]), np.sum(im[:,0]), np.sum(im[:,s[1]-1])])/255

    checkVals = np.concatenate([sumLines[0:2] > float(s[0])/3.0, sumLines[2:4] > float(s[1])/3.0], axis = 0)
    checkValsMini = np.concatenate([sumLines[0:2] < float(s[0])/5.0, sumLines[2:4] < float(s[1])/5.0], axis = 0)
    
    sumVal = np.sum(checkVals)
    sumValMini = np.sum(checkValsMini)

    if (sumVal > 2) or (np.sum(checkVals[0:2]) == 2) or (np.sum(checkVals[2:4] == 2)) :
        #Improve the size
        squareSize[0] = np.min([squareSize[0]+sizeInc, fullSize[0]-1, squareSize[1]+sizeInc, fullSize[1]-1])
        if(squareSize[0] != squareSize[1]):
            squareSize[1] = squareSize[0]
            squareOffset[1] = max(0, squareOffset[1]-int(sizeInc/2))
            squareOffset[0] = max(0,squareOffset[0]-int(sizeInc/2))     


    elif sumVal > 0 :
        #Find the sides
        ind = np.argwhere(checkVals)
        #Move the square
        for k in ind :
            if k == 0 :
                squareOffset[0] = max(0,squareOffset[0]-moveInc)
            elif k == 1 :
                squareOffset[0] = min(squareOffset[0]+moveInc, fullSize[0]-1-squareSize[0])
            elif k == 2 :
                squareOffset[1] = max(0, squareOffset[1]-moveInc)
            elif k == 3 :
                squareOffset[1] = min(squareOffset[1]+moveInc, fullSize[1]-1-squareSize[1])

    if (sumValMini > 2) or (np.sum(checkValsMini[0:2]) == 2) or (np.sum(checkValsMini[2:4] == 2)) :
        squareSize[0] = max(100, squareSize[0]-sizeInc)
        if(squareSize[0] != squareSize[1]):
            squareSize[1] = squareSize[0]
            squareOffset[1] = min(squareOffset[1]+int(sizeInc/2), fullSize[1]-1-squareSize[1])
            squareOffset[0] = min(squareOffset[0]+int(sizeInc/2), fullSize[0]-1-squareSize[0])
        

    return squareOffset, squareSize


def LookForHand(sFrame):

    squareSize = np.array([0,0])
    squareOffset = np.array([0,0])
    squareSize[0] = min(sFrame[0], sFrame[1])
    squareSize[1] = squareSize[0]
    squareOffset[0] = 0
    squareOffset[1] = int((sFrame[1] - squareSize[1])/2)
    
    return squareOffset, squareSize
