#move the window based on the location of the bounding box

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

def onTrack7(val):
    global hueLow2
    hueLow2=val
    print('Hue Low 2', hueLow2)

def onTrack8(val):
    global hueHigh2
    hueHigh2=val
    print('Hue High 2', hueHigh2)

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
hueLow2=10
hueHigh2=20

#implementing trackbars. Remember, all trackbars start at zero. the first number is just the default start value.
cv2.namedWindow('myTracker')
cv2.moveWindow('myTracker',width,0)
cv2.createTrackbar('Hue Low',"myTracker",10,179,onTrack1)
cv2.createTrackbar('Hue High',"myTracker",20,179,onTrack2)
cv2.createTrackbar('Hue Low 2',"myTracker",10,179,onTrack7)
cv2.createTrackbar('Hue High 2',"myTracker",20,179,onTrack8)
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
    lowerBound2=np.array([hueLow2,satLow,valLow])
    upperBound2=np.array([hueHigh2,satHigh,valHigh])
    #magic happens! myMask is an array that is the same size as frameHSV but it only shows pixes between the tolerances of upper and lower bound arrays
    myMask=cv2.inRange(frameHSV, lowerBound, upperBound) #if pixel is in range it will be white. if it is not in range, it will be black
    myMask2=cv2.inRange(frameHSV, lowerBound2, upperBound2)
    myMaskComposite=myMask|myMask2 #the | icon is an OR operator

    contours,junk=cv2.findContours(myMask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #the mask is a white spot against a black backround
    #cv2.drawContours(frame,contours,-1,(255,0,0),3) #-1 says draw all. if you say 0 it shows the first, 1 is the second, etc
    
    for contour in contours: #loop goes through all the subarrays and only displays ones greater than 100 to kill off noise
        area=cv2.contourArea(contour)
        if area>=200:
            #cv2.drawContours(frame,[contour],0,(255,0,0),3) #draws the perimeter
            x,y,w,h=cv2.boundingRect(contour) #draw a bounding box. xy defines upper left anchor point. then
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)
            xPOS=0
            yPOS=0
            xPOS=x
            yPOS=y
            xPOS=int(xPOS/width*2560)
            yPOS=int(yPOS/height*1440)
   

    #myMaskComp=cv2.add(myMask,MyMask2) An alternative way of creating a composite. 
    #myMask=cv2.bitwise_not(myMask)#this makes whatever is in the range of the sliders get rejected
    #making an AND pixel from frame and the mask. output shows the fame but not pixels that are masked
    myObject=cv2.bitwise_and(frame,frame,mask=myMaskComposite)
    myobjectSmall=cv2.resize(myObject,(int(width/2),int(height/2)))
    cv2.imshow('My Object', myobjectSmall)
    cv2.moveWindow('My Object',xPOS,yPOS)
    myMaskSmall=cv2.resize(myMask,(int(width/2),int(height/2)))
    cv2.imshow('my Mask', myMaskSmall)
    cv2.moveWindow('my Mask', 0, height)
    myMaskSmall2=cv2.resize(myMask2,(int(width/2),int(height/2)))
    cv2.imshow('my Mask 2', myMaskSmall2)
    cv2.moveWindow('my Mask 2', 0, height+int(height/2)+30)

    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam', 0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()

#we are making 6 trackbars for HSV 