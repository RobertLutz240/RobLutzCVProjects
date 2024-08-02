#detect hand gestures and label them

import cv2
print(cv2.__version__)
import numpy as np
import time

class mpHands:
    import mediapipe as mp
    def __init__(self,maxHands=2,tol1=int(.5), tol2=int(.5)):
        self.hands=self.mp.solutions.hands.Hands(False,maxHands,tol1,tol2)
    def Marks(self,frame):
        myHands=[]
        handsType=[]
        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=self.hands.process(frameRGB)
        if results.multi_hand_landmarks != None:
            for hand in results.multi_handedness:
                handType=hand.classification[0].label
                handsType.append(handType)
            for handLandMarks in results.multi_hand_landmarks:
                myHand=[]
                for landMark in handLandMarks.landmark:
                    myHand.append((int(landMark.x*width),int(landMark.y*height)))
                myHands.append(myHand)
        return myHands,handsType #myHands is the array of landmarks. handsType is the label saying whether L or R

def findDistances(handData):
    distMatrix=np.zeros([len(handData),len(handData)],dtype='float')
    for row in range(0,len(handData)):
        for column in range(0,len(handData)):
            distMatrix[row][column]=((handData[row][0]-handData[column][0])**2+(handData[row][1]-handData[column][1])**2)**(1./2.)
    return distMatrix #distance between a point (one array for each point's distance to each other point)

def findError(gestureMatrix,unknownMatrix,keyPoints):
    error=0
    for row in keyPoints:
        for column in keyPoints:
            error=error+abs(gestureMatrix[row][column]-unknownMatrix[row][column])
    return error #a numbr totalling the distance between the points and the gesture matrix and the (currently visible) hand matrix

def findGesture(unknownGesture,knownGesture,keyPoints,gestNames,tol): #we've trained known gestures, now we give it unknown gesture (out live hand feed)
    errorArray=[]
    for i in range(0,len(gestNames),1): #this steps through each gesture
        error=findError(knownGesture[i],unknownGesture,keyPoints) #calls the function to find error and cycles through the known gestures while comparing them to the live hand feed (unnkown gesture)
        errorArray.append(error) #creates an array of the "error" for the current gesture relative to each of the known gestures 
    errorMin=errorArray[0] #need to assign to an index, but will later correct it.
    minIndex=0 #variable for keeping track of the index
    for i in range(0,len(errorArray),1): #loop to seek minimum error
        if errorArray[i]<errorMin: #checks to see if the current sum of distances is less than the current minimum sum of distances
            errorMin=errorArray[i] #updates the error min to be the new, smaller reported errorArray if it is smaller.
            minIndex=i #updates the index to reflect the new minimum
    if errorMin<tol:
        gesture=gestNames[minIndex]
    if errorMin>=tol:
        gesture="Unknown"
    return gesture

time.sleep(3)
width=1280
height=720
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
findHands=mpHands(1)
font=cv2.FONT_HERSHEY_SIMPLEX
color=(0,0,255)
fontScale=1
fontThickness=2
lowerLimit=0
upperLimit=468

keyPoints=[0,4,5,8,9,12,13,16,17,20] #array of points on hand, derived from results.multi_hand_landmarks
train=True #first time thru while loop go down "train" pipeline
tol=1500 #arbitrary tolerance value
trainCnt=0
knownGestures=[]

numGest=int(input("how many gestures do you want? ")) #number of gestures
gestNames=[] #names of gestures
for i in range(0,numGest,1): #we dont knot how many gestures someone will want to encode, so this is flexible. range(start,end,increment) fyi
    prompt='Name of Gesture # '+str(i+1)+" " #it has asked how many gestures to encode, now it will ask you to name each one. This line just shows you what number gesture you are encoding
    name=input(prompt) #taking user input and assigning it to name
    gestNames.append(name) #taking user input from name and appending the gestNames array. 
print(gestNames)

while True:
    ignore, frame = cam.read()
    handsLM,handsType=findHands.Marks(frame) #findhands is a mediapipe object. marks in the method inside. marks analyses frame looking for hands. 
    if train==True:
        if handsLM!=[]: #handslm will be empty if there is no hand in the frame.
            print('Please show gesture', gestNames[trainCnt],': press t when ready') 
            if cv2.waitKey(1) & 0xff == ord('t'):
                knownGesture=findDistances(handsLM[0]) #known gesture is an array of distances between each of the points.
                knownGestures.append(knownGesture) #builds array of known gestures
                trainCnt=trainCnt+1
                if trainCnt==numGest:
                    train=False #set training to false once youve trained the number of gestures youve typed in
                #print(knownGesture)
    if train == False:
        if handsLM !=[]:
            unknownGesture=findDistances(handsLM[0])
            myGesture=findGesture(unknownGesture,knownGestures,keyPoints,gestNames,tol) #known gestures are made while training=true. unknown gesture is live feed using finddistances.
            #error=findError(knownGesture,unknownGesture,keyPoints) #not using this anymore because it is done in findgesture
            cv2.putText(frame,str(myGesture),(100,225),font,fontScale,color,fontThickness)
            #cv2.putText(frame,str(int(error)),(100,175),font,fontScale,color,fontThickness)
    for hand,handType in zip(handsLM,handsType): #manipulating data from calling hand data
        if handType=='Right':
            lbl='Right'
        if handType=='Left':
            lbl='Left'
        count=0
        for x in handsLM:
            for landmark in keyPoints:
                cv2.putText(frame,str(landmark),handsLM[count][landmark],font,fontScale,color,fontThickness)
            count=count+1
    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam',0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()
