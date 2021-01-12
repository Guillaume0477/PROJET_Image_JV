import numpy as np
import cv2
import os
import DetectParams

def GetParametersFromFiles(file):
    im = cv2.imread(file, cv2.IMREAD_GRAYSCALE)

    id1 = file.rfind('_')
    id2 = file.rfind('.')
    label = int(file[id1+1:id2])

    params = DetectParams.getParameters(im, im)

    return label, params

def GetParametersFromDir(dirPath):
    #Read data path
    listFiles = [dirPath + f for f in os.listdir(dirPath) if f.endswith(".png")]
    
    #Initialize Labels and parameters associated
    L = []
    Params = []

    for f in listFiles :
        #Get the label and the parameters of each file
        label, params = GetParametersFromFiles(f)

        #Concatenate labels and parameters
        L.append(label)
        Params.append(params)

    return L, Params

def main():
    #Path where images are located
    pathToRead = "Images/"

    L, Params = GetParametersFromDir(pathToRead)

    print(Params, L)

main()