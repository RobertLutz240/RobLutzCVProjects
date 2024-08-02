#add FPS counter
#box face in a red box
#box eyes in a blue box


import cv2
import time
print(cv2.__version__)
width=1280
height=720
FPS= " FPS"
framesPerSecond=0
tLast=time.time()
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

faceCascade=cv2.CascadeClassifier('C:/Users/nedm5/Documents/PythonVE/haar/haarcascade_frontalface_default.xml')
eyeCascade=cv2.CascadeClassifier("C:/Users/nedm5/Documents/PythonVE/haar/haarcascade_eye.xml")

time.sleep(0.1)
fpsFILT=30

while True:
    dT=time.time()-tLast
    tLast=time.time()
    fps=1/dT
    fpsFILT=fpsFILT*0.9+fps*0.1
    ignore, frame = cam.read()
    #greyscale images are faster to process
    frameGray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(frameGray,1.3,5)#finds faces and puts their position in the variable faces
    eyes=eyeCascade.detectMultiScale(frameGray,1.5,5)
    #print(faces) #faces in image returns an array of arrays. each array is the position of one face.
    for face in faces:
        x,y,w,h=face
        #print("x= ", x, "y= ", y, "w= ", w, "h= ", h)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)
        frameROI=frame[y:y+h,x:x+w]
        frameROIGray=cv2.cvtColor(frameROI,cv2.COLOR_BGR2GRAY)
        eyes=eyeCascade.detectMultiScale(frameROIGray) #this limits the search for eyes to inside a face.
        for eye in eyes:
            xeye,yeye,weye,heye=eye
            print("x= ", xeye, "y= ", yeye, "w= ", weye, "h= ", heye)
            cv2.rectangle(frame[y:y+h,x:x+w],(xeye,yeye),(xeye+yeye,yeye+heye),(255,0,0),3) #frame is being subset based on the xywh if a face

#for eye in eyes: removed to embed in face only 
#    x,y,w,h=eye
#print("x= ", x, "y= ", y, "w= ", w, "h= ", h)
    #    cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),3)
    cv2.putText(frame, str(int(fpsFILT))+FPS,(int(width*0.75),int(height*0.075)),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),1)
    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam', 0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()