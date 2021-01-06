import cv2

def Cleaning(im):
    
    structElemEro = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    structElemDil = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))

    im = cv2.erode(im, structElemEro)
    im = cv2.dilate(im, structElemDil)

    return im
