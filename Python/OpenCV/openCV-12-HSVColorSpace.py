import cv2
import numpy as np
print(cv2.__version__)
evt=0
xVal=0
yVal=0
def mouseClick(event, xPOS, yPOS, flags, params):
    global evt
    global xVal
    global yVal
    if event == cv2.EVENT_LBUTTONDOWN:
        print(event)
        xVal=xPOS
        yVal=yPOS
        evt=event
    if event==cv2.EVENT_RBUTTONUP:
        evt=event
        print(event)
width=1280
height=720
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cv2.namedWindow('my WEBcam')
cv2.setMouseCallback('my WEBcam', mouseClick)
while True:
    ignore, frame = cam.read()
    if evt==1:
        x=np.zeros([height,width,3], dtype=np.uint8)
        y=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        #clr=frame[yVal][xVal] retired for variable y which converts to HSV
        clr=y[yVal][xVal]
        print(clr)
        x[:,:]=clr
        cv2.putText(x,str(clr),(0,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),1)
        cv2.imshow('Color Picker', x)
        evt=0
        cv2.moveWindow('Color Picker',width,0)
    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam', 0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()



#HSV colorspace is Hue, Saturation, Value
#still 3 numbers, same data but HSV computer looks at the color much more like we humans see it.
#Hue is an angle on the colorwheel. think 0 to 360. Hue is color as we think of it
#Saturation is how intense the color is. Max saturation is 255. Dilution of the "ink" approaches 0 as max dilution
#Value is adding black. max value is Black.
#Saturation of zero is greyscale
#in open cv 0 on saturation is clear and 255 is the edge (full saturation)
#in open cv 0 is black, 255 is no blackness
#in open cv hue is an angle. it is 0 to 180. couldnt be 360 because that doesnt fit in 255 for 8bit int
# 0 and 179 are really close. opposite is 90
#opposite of 45 is 135 on the circle