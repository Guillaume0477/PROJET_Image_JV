import numpy as np

def trackHand(im, squareOffset, squareSize, fullSize):

    #Increment when moving of resizing the square
    moveInc = 20
    sizeInc = 20

    im = np.array(im)
    s = np.shape(im)

    #Bounds of the square
    xmin = squareOffset[0]
    xmax = squareOffset[0] + squareSize[0]
    ymin = squareOffset[1]
    ymax = squareOffset[1] +  squareSize[1]

    #Get the number of 1s on the borders of the square
    sumLines = np.array([np.sum(im[10,:]), np.sum(im[s[0]-10,:]), np.sum(im[:,10]), np.sum(im[:,s[1]-10])])/255

    #Check if there are to many border values or not enough
    checkVals = np.concatenate([sumLines[0:2] > float(s[0])/10.0, sumLines[2:4] > float(s[1])/10.0], axis = 0)
    checkValsMini = np.concatenate([sumLines[0:2] < float(s[0])/15.0, sumLines[2:4] < float(s[1])/15.0], axis = 0)
    sumVal = np.sum(checkVals)
    sumValMini = np.sum(checkValsMini)
    
    #Check if there are 3 sides with to many values, of if opposed sides have to many values
    if (sumVal > 2) or (np.sum(checkVals[0:2]) == 2) or (np.sum(checkVals[2:4]) == 2) :
        #Improve the size
        squareSize[0] = np.min([squareSize[0]+sizeInc, fullSize[0]-1, squareSize[1]+sizeInc, fullSize[1]-1])
        if(squareSize[0] != squareSize[1]):
            squareSize[1] = squareSize[0]
            squareOffset[1] = max(0, squareOffset[1]-int(sizeInc/2))
            squareOffset[0] = max(0,squareOffset[0]-int(sizeInc/2))     

    #Check if a move is needed
    elif sumVal > 0 :
        #Find the sides
        ind = np.argwhere(checkVals)
        #Move the square
        for k in ind :
            #up
            if k == 0 :
                squareOffset[0] = max(0,squareOffset[0]-moveInc)
            #down
            elif k == 1 :
                squareOffset[0] = min(squareOffset[0]+moveInc, fullSize[0]-1-squareSize[0])
            #left
            elif k == 2 :
                squareOffset[1] = max(0, squareOffset[1]-moveInc)
            #right
            elif k == 3 :
                squareOffset[1] = min(squareOffset[1]+moveInc, fullSize[1]-1-squareSize[1])

    #Check if there are 3 sides with not enough values, or if opposed sides have to many values
    elif (sumValMini > 2) or (np.sum(checkValsMini[0:2]) == 2) or (np.sum(checkValsMini[2:4]) == 2) :
        #Decrease size
        squareSize[0] = max(100, squareSize[0]-sizeInc)
        if(squareSize[0] != squareSize[1]):
            squareSize[1] = squareSize[0]
            squareOffset[1] = min(squareOffset[1]+int(sizeInc/2), fullSize[1]-1-squareSize[1])
            squareOffset[0] = min(squareOffset[0]+int(sizeInc/2), fullSize[0]-1-squareSize[0])
        

    return squareOffset, squareSize


def LookForHand(sFrame):
    #Resize the square at maximum value to find hand
    squareSize = np.array([0,0])
    squareOffset = np.array([0,0])
    squareSize[0] = min(sFrame[0]-1, sFrame[1]-1)
    squareSize[1] = squareSize[0]
    squareOffset[0] = 0
    squareOffset[1] = int((sFrame[1] - squareSize[1])/2)
    
    return squareOffset, squareSize
