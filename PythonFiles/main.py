import Calibrage
import cv2
import matplotlib.pyplot as plt

def main():
    cap = cv2.VideoCapture(-1)

    while True :
        ret,frame = cap.read()

        cv2.imshow('Capture Video', frame)

        #Capture interaction utilisateur
        key = cv2.waitKey(1) #on évalue la touche pressée
        plt.pause(0.001)
        plt.cla()
        if key & 0xFF == ord('q'): #si appui sur'q'
            break #sortie de la boucle while

    cap.release()
    cv2.destroyAllWindows()
    return 0


main()