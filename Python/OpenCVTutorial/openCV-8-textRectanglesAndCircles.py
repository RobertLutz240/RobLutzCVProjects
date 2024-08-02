import cv2
import time

print(cv2.__version__)
width=1280
height=720
counter = 0
FPS= " FPS"
framesPerSecond=0
timer=time.strftime("%S", time.localtime())
timer2=timer

cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'M','J','P','G'))
while True:
    if timer2==timer:
        ignore, frame = cam.read()
        #frame[0:420,280:360]=(0,0,255)
        cv2.rectangle(frame,(int(width*0.33),int(height*0.33)),(int(width*0.66),int(height*0.66)),(0,255,0),2)
        cv2.circle(frame,(int(width/2),int(height/2)),25,(0,0,255),2)
        cv2.putText(frame, str(timer),(int(width*0.01),int(height*0.075)),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),1)
        cv2.putText(frame, str(counter),(int(width*0.01),int(height*0.15)),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),1)
        cv2.putText(frame, str(framesPerSecond)+FPS,(int(width*0.75),int(height*0.075)),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),1)
        cv2.imshow('my WEBcam', frame)
        cv2.moveWindow('my WEBcam', 0,0)
        counter=counter+1
        timer=time.strftime("%S", time.localtime())
    else:
        framesPerSecond=counter
        cv2.putText(frame, str(framesPerSecond)+FPS,(int(width*0.75),int(height*0.075)),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),1)
        counter=0
        timer=time.strftime("%S", time.localtime())
        timer2=timer

    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()