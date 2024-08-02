import cv2
import numpy as np
print(cv2.__version__)
width=1280
height=720
B=0
G=0
R=0
H=0
S1=0
V1=0
S2=255
V2=255
xPOS=0
yPOS=0
toggler=0
widthIncrement=int(width/(180))
heightIncrement=int(height/(255))
#HSVIncrement=int(255/180)
saturationWindow=np.zeros([height,width,3], dtype=np.uint8)
valueWindow=np.zeros([height,width,3], dtype=np.uint8)
for column in range(0,179):
        xPOS=xPOS+widthIncrement
        H=H+1
        for row in range(0,254):
                yPOS=yPOS+heightIncrement
                saturationWindow[0:height,xPOS:xPOS+widthIncrement]=H,S1,V1
                valueWindow[0:height,xPOS:xPOS+widthIncrement]=H,S2,V2
                S1=S1+1
                V1=V1+1
                S2=S2-1
                V2=V2-1

while True:
    #satHSV=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    #valHSV=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    HSV=cv2.cvtColor(saturationWindow,cv2.COLOR_BGR2HSV)
    HSV2=cv2.cvtColor(valueWindow,cv2.COLOR_BGR2HSV)
    cv2.imshow('saturation', HSV)
    cv2.moveWindow('saturation',0,0)
    cv2.imshow('value', HSV2)
    cv2.moveWindow('value',width,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

#need to make an empty array for the frame
#need to move from 0-180 Hue on the columns axis
#need to move from 0-255 Saturation/Value on the rows axis
#make two windows
#top window goes through the colors with 0-255 saturation
#bottom window goes through the colors with 0-255 value