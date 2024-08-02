#make a class from the code below

import cv2
print(cv2.__version__)

class mpFace:
    import mediapipe as mp
    def __init__(self):
        self.findFace=self.mp.solutions.face_detection.FaceDetection()
    def Marks(self,frame):
        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=self.findFace.process(frameRGB)
        faceBoundBoxs=[]
        if results.detections != None:
            for face in results.detections:
            #drawFace.draw_detection(frame,face)
                bBox=face.location_data.relative_bounding_box
                topLeft=(int(width*(bBox.xmin)),int(height*(bBox.ymin)))
                bottomRight=(int(width*(bBox.xmin+bBox.width)),int(height*(bBox.ymin+bBox.height)))
                cv2.rectangle(frame,topLeft,bottomRight,(255,0,0),3)
                faceBoundBoxs.append((topLeft,bottomRight))
        return faceBoundBoxs

class mpPose:
    import mediapipe as mp
    def __init__(self,still=False,complexity=True,smoothLandmarks=True,enableSegmentation=True, smoothSegmentation=True, tol1=int(.5), tol2=int(.5)): #False,0,True,True,True,int(0.5),int(0.5)
        self.myPose=self.mp.solutions.pose.Pose(still,complexity,smoothLandmarks,enableSegmentation,smoothSegmentation,tol1,tol2)
    def Marks(self,frame):
        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=self.myPose.process(frameRGB)
        poseLandmarks=[]
        if results.pose_landmarks:
            for lm in results.pose_landmarks.landmark:     
                poseLandmarks.append((int(lm.x*width),int(lm.y*height)))
        return poseLandmarks

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
                #print(hand)
                #print(hand.classification)
                #print(hand.classificationp[0])
                handType=hand.classification[0].label
                handsType.append(handType)
            for handLandMarks in results.multi_hand_landmarks:
                myHand=[]
                for landMark in handLandMarks.landmark:
                    myHand.append((int(landMark.x*width),int(landMark.y*height)))
                myHands.append(myHand)
        return myHands,handsType #myHands is the array of landmarks. handsType is the label saying whether L or R

width=1280
height=720
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
fastFaceDetect=mpFace()
findHands=mpHands(2)
findPose=mpPose()
font=cv2.FONT_HERSHEY_SIMPLEX
color=(0,0,255)
fontScale=2
fontThickness=2
while True:
    ignore, frame = cam.read()
    handsLM,handsType=findHands.Marks(frame) #find ahands is mediapipe object. marks in the method inside. marks analyses frame looking for hands. 
    faceLoc=fastFaceDetect.Marks(frame)
    poseLM=findPose.Marks(frame)
    if poseLM != []: #manipulating data from the pose class
        for index in [0,2,5,9,10]:
                cv2.circle(frame,poseLM[index],20,color,-1)
    for face in faceLoc: #manipulating data from the face class
        cv2.rectangle(frame,face[0],face[1],color,fontThickness)
    for hand,handType in zip(handsLM,handsType): #manipulating data from calling hand data
        if handType=='Right':
            lbl='Right'
        if handType=='Left':
            lbl='Left'
        cv2.putText(frame,lbl,hand[8],font,fontScale,color,fontThickness)
    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam', 1000,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()


