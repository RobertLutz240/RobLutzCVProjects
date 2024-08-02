import cv2
import numpy as np
print(cv2.__version__)


#implementing functions for trackbars
def onTrack1(val):
    global hueLow
    hueLow=val
    print('Hue Low ', hueLow)

def onTrack2(val):
    global hueHigh
    hueHigh=val
    print('Hue High ', hueHigh)

def onTrack3(val):
    global satLow
    satLow=val
    print('Sat Low ', satLow)

def onTrack4(val):
    global satHigh
    satHigh=val
    print('Sat High ', satHigh)

def onTrack5(val):
    global valLow
    valLow=val
    print('Val Low ', valLow)

def onTrack6(val):
    global valHigh
    valHigh=val
    print('Val High ', valHigh)

width=640
height=360
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

#Seeding initial values
hueLow=10
hueHigh=20
satLow=10
satHigh=250
valLow=10
valHigh=250

#implementing trackbars. Remember, all trackbars start at zero. the first number is just the default start value.
cv2.namedWindow('myTracker')
cv2.moveWindow('myTracker',width,0)
cv2.createTrackbar('Hue Low',"myTracker",10,179,onTrack1)
cv2.createTrackbar('Hue High',"myTracker",20,179,onTrack2)
cv2.createTrackbar('Sat Low',"myTracker",10,255,onTrack3)
cv2.createTrackbar('Sat High',"myTracker",250,255,onTrack4)
cv2.createTrackbar('Val Low',"myTracker",10,255,onTrack5)
cv2.createTrackbar('Val High',"myTracker",250,255,onTrack6)


while True:
    ignore, frame = cam.read()

    #creating a new frame in the HSV colorspace
    frameHSV=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #create a box of low values and high values that is limited to pixels in the values set by sliders
    lowerBound=np.array([hueLow,satLow,valLow])
    upperBound=np.array([hueHigh,satHigh,valHigh])
    #magic happens! myMask is an array that is the same size as frameHSV but it only shows pixes between the tolerances of upper and lower bound arrays
    myMask=cv2.inRange(frameHSV, lowerBound, upperBound) #if pixel is in range it will be white. if it is not in range, it will be black
    #myMask=cv2.bitwise_not(myMask)#this makes whatever is in the range of the sliders get rejected
    #making an AND pixel from frame and the mask. output shows the fame but not pixels that are masked
    myObject=cv2.bitwise_and(frame,frame,mask=myMask)
    myobjectSmall=cv2.resize(myObject,(int(width/2),int(height/2)))
    cv2.imshow('My Object', myobjectSmall)
    cv2.moveWindow('My Object',int(width/2),int(height))
    cv2.imshow('my Mask', myMask)
    cv2.moveWindow('my Mask', 0,height)
    #optional resizing
    myMaskSmall=cv2.resize(myMask,(int(width/2),int(height/2)))

    cv2.imshow('my Mask', myMaskSmall)
    cv2.moveWindow('my Mask', 0, height)

    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam', 0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()

#we are making 6 trackbars for HSV 