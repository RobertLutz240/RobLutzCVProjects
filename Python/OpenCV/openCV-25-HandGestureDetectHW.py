#detect hand gestures and label them

import cv2
print(cv2.__version__)
import numpy as np

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
                handType=hand.classification[0].label
                handsType.append(handType)
            for handLandMarks in results.multi_hand_landmarks:
                myHand=[]
                for landMark in handLandMarks.landmark:
                    myHand.append((int(landMark.x*width),int(landMark.y*height)))
                myHands.append(myHand)
        return myHands,handsType #myHands is the array of landmarks. handsType is the label saying whether L or R

class mpFaceMesh:
    import mediapipe as mp
    def __init__(self,still=False,numFaces=1,a=True,tol1=int(.5),tol2=int(.5),drawMesh=True):
        self.myFaceMesh=self.mp.solutions.face_mesh.FaceMesh(still,numFaces,a,tol1,tol2) #object we use to computate our facemesh (static,number of face,tacking)
        self.myDraw=self.mp.solutions.drawing_utils
        self.draw=drawMesh
    def Marks(self,frame):
        global width
        global height
        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=self.myFaceMesh.process(frameRGB)
        facesMeshLandmarks=[] #array for storing multiple faces
        if results.multi_face_landmarks != None:
           for faceMesh in results.multi_face_landmarks: #move through each face of multiple faces
                faceMeshLandmarks=[] #singular array of landmarks for a face
                for lm in faceMesh.landmark: #move through each landmark in a face
                    loc=(int(lm.x*width),int(lm.y*height)) #normalize coordinates for each landmark in a face
                    faceMeshLandmarks.append(loc) # populate singular array of landmarks for a face
                facesMeshLandmarks.append(faceMeshLandmarks)
                if self.draw==True:
                    self.myDraw.draw_landmarks(frame,faceMesh) #AKA self.mp.solutions.drawing_utils.draw_landmarks(frame,faceMesh). faceMesh because it has the raw facedata as mp expects it (pre our simplification)
        return facesMeshLandmarks

def findDistances(handData):
    distMatrix=np.zeros([len(handData),len(handData)],dtype='float')
    for row in range(0,len(handData)):
        for column in range(0,len(handData)):
            distMatrix[row][column]=((handData[row][0]-handData[column][0])**2+(handData[row][1]-handData[column][1])**2)**(1./2.)
    return distMatrix

def findError(gestureMatrix,unknownMatrix,keyPoints):
    error=0
    for row in keyPoints:
        for column in keyPoints:
            error=error+abs(gestureMatrix[row][column]-unknownMatrix[row][column])
    return error    

width=1280
height=720
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
fastFaceDetect=mpFace()
findHands=mpHands(1)
findPose=mpPose()
findFaceMesh=mpFaceMesh(drawMesh=False)
font=cv2.FONT_HERSHEY_SIMPLEX
color=(0,0,255)
fontScale=1
fontThickness=2
lowerLimit=0
upperLimit=468

def setLower(value):
    global lowerLimit
    lowerLimit=value

def setUpper(value):
    global upperLimit
    upperLimit=value

cv2.namedWindow('Trackbars')
cv2.moveWindow('Trackbars',width+50,0)
cv2.resizeWindow('Trackbars',400,150)

cv2.createTrackbar('lowerLimit','Trackbars',0,468,setLower)
cv2.createTrackbar('upperLimit','Trackbars',468,468,setUpper)

keyPoints=[0,4,5,8,9,12,13,16,17,20] #array of points on hand, derived from results.multi_hand_landmarks
train=True #first time thru while loop go down "train" pipeline
while True:
    ignore, frame = cam.read()
    handsLM,handsType=findHands.Marks(frame) #findhands is a mediapipe object. marks in the method inside. marks analyses frame looking for hands. 
    if train==True:
        if handsLM!=[]: #handslm will be empty if there is no hand in the frame.
            print('Show your gesture, press T when ready ') 
            if cv2.waitKey(1) & 0xff == ord('t'):
                knownGesture=findDistances(handsLM[0]) #known gesture is an array of distances between each of the points.
                train=False #set training to false once youve trained it
                print(knownGesture)
    if train == False:
        if handsLM !=[]:
            unknownGesture=findDistances(handsLM[0])
            error=findError(knownGesture,unknownGesture,keyPoints)
            cv2.putText(frame,str(int(error)),(100,175),font,fontScale,color,fontThickness)
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
