import cv2
print(cv2.__version__)

rows=int(input('how many rows? '))
columns=int(input('how many columns? '))

width=1280
height=720
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'M','J','P','G'))
while True:
    ignore, frame = cam.read()
    frame=cv2.resize(frame,(int(width/columns),int(height/columns)))
    for i in range(0,rows):
        for j in range(0,columns):
            windowName='Window'+str(i)+' x '+str(j)
            cv2.imshow(windowName,frame)
            cv2.moveWindow(windowName,int((width/columns)*j),int((height/columns+30)*i))


    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam', 0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()