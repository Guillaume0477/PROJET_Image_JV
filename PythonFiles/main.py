import Calibrage
import cv2
import matplotlib.pyplot as plt

def main():
    cap = cv2.VideoCapture(0)

    while True :
        ret,frame = cap.read()

        key = cv2.waitKey(1)

        if key & 0xFF == ord('q'):
            break


        cv2.imshow('Capture Video', frame)

    cap.release()
    cv2.destroyAllWindows()
    return 0


main()