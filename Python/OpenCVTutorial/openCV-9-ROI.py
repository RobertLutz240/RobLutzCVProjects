import cv2
print(cv2.__version__)
width=640
height=360
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
while True:
    ignore, frame = cam.read()
    frameROI=frame[150:210,250:390] # 1 creates a frame of a subset of the main frame
    frameROIGray=cv2.cvtColor(frameROI, cv2.COLOR_BGR2GRAY) # 2 converts the subset frame to greyscale
    frameROIBGR=cv2.cvtColor(frameROIGray,cv2.COLOR_GRAY2BGR) # grayscale arrays have 1 datapoint. BGR have 3 color datapoints. 

    frame[150:210,250:390]=frameROI # superimposes the greyscale subset to the frame
    frame[0:60,0:140]=frameROIBGR

    cv2.imshow('my BGR ROI', frameROIBGR)
    cv2.moveWindow('my BGR ROI', 650,180)


    cv2.imshow('my Gray ROI', frameROIGray) # 3 creates a new window displaying the greyscale frame
    cv2.moveWindow('my Gray ROI', 650,90) # 4 moves the new window 
    cv2.imshow('my ROI', frameROI)
    cv2.moveWindow('my ROI', 650,0)
    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam', 0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()