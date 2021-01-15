import numpy as np
import cv2
import os
import DetectParams
from sklearn import svm, metrics
from sklearn.multiclass import OneVsOneClassifier, OneVsRestClassifier

def GetParametersFromFiles(file):
    #Read the image
    im = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    #Get indexes of the label and extract the label
    id1 = file.rfind('_')
    id2 = file.rfind('.')
    label = int(file[id1+1:id2])
    # print(label)
    #Get the parameters from the image
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
    pathToRead = "TrainImages2/"
    pathToReadTest = "TestImages2/"

    #Get the labels and parameters to train the SVM
    L, Params = GetParametersFromDir(pathToRead)
    LTest, ParamsTest = GetParametersFromDir(pathToReadTest)

    #Reshape l'organisation des données
    Params = np.reshape(Params, [np.shape(Params)[0], np.shape(Params)[2]])
    ParamsTest = np.reshape(ParamsTest, [np.shape(ParamsTest)[0], np.shape(ParamsTest)[2]])

    #Creation de la SVM
    mySVM = OneVsRestClassifier(svm.SVC(kernel = 'linear'))
    mySVM.fit(Params, L)

    Pred = mySVM.predict(ParamsTest)

    print(LTest)
    print(Pred)
    print(metrics.classification_report(LTest, Pred))

    return 0

main()