import Calibrage
import cv2
import matplotlib.pyplot as plt

def main():
    #Config cam
    cap = cv2.VideoCapture(0)
    play = True


    colorHand, BBoxHand = Calibrage.HandCalibrate(cap)


    while play :
        #Get the frame
        ret,frame = cap.read()


        #Detect user quit command
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            play = False

        #Show the frame
        cv2.imshow('Capture Video', frame)

    #Destroy windows
    cap.release()
    cv2.destroyAllWindows()
    return 0


main()