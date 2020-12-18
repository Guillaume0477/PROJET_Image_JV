import cv2

def HandCalibrate(cap):

    print("Put your hand inside the square and push 'A'")

    acq = True

    squareSize = [100,100]
    squareOffset = [200,200]

    while acq :
        #Get the frame
        ret,frame = cap.read()


        #Detect user quit command
        key = cv2.waitKey(1)

        if key == ord('g'):



            #End the calibration
            acq = False

        #Move the square left
        elif key == ord('q'):
            squareOffset[1] -= 10
        #Move the square right
        elif key == ord('d'):
            squareOffset[1] += 10
        #Move the square up
        elif key == ord('z'):
            squareOffset[0] -= 10
        #Move the square down
        elif key == ord('s'):
            squareOffset[0] += 10
        #Increase square size
        elif key == ord('a'):
            squareSize[0] -= 20
            squareSize[1] -= 20
            squareOffset[1] += 10
            squareOffset[0] += 10
        #Reduce square size
        elif key == ord('e'):
            squareSize[0] += 20
            squareSize[1] += 20
            squareOffset[1] -= 10
            squareOffset[0] -= 10            

        #Show the frame
        frame[squareOffset[0]:squareOffset[0]+squareSize[0],squareOffset[1],:] = 255
        frame[squareOffset[0]:squareOffset[0]+squareSize[0],squareOffset[1]+squareSize[1],:] = 255
        frame[squareOffset[0],squareOffset[1]:squareOffset[1] + squareSize[1],:] = 255 
        frame[squareOffset[0]+squareSize[0],squareOffset[1]:squareOffset[1] + squareSize[1],:] = 255 



        cv2.imshow('Calibrate your hand', frame)

    #Destroy windows
    cap.release()
    cv2.destroyAllWindows()

    return [0,0,0], [[0,0], [1,1]]
