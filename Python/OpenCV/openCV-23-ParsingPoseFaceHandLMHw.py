#take hw from 22 and make a class for facelandmarks
#in the main program zero in and map out which landmarks are for which parts. use subset arrays [0-468]
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
findFaceMesh=mpFaceMesh(drawMesh=False)
font=cv2.FONT_HERSHEY_SIMPLEX
color=(0,0,255)
fontScale=0.2
fontThickness=1

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

while True:
    ignore, frame = cam.read()
    handsLM,handsType=findHands.Marks(frame) #find ahands is mediapipe object. marks in the method inside. marks analyses frame looking for hands. 
    faceLoc=fastFaceDetect.Marks(frame)
    poseLM=findPose.Marks(frame)
    facesMeshLM=findFaceMesh.Marks(frame)
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
    for faceMeshLM in facesMeshLM: #face singular is stepping through facesMeshLM=findFaceMesh.Marks(frame)
        cnt=0
        for lm in faceMeshLM:
            if cnt>=lowerLimit and cnt<=upperLimit:
                cv2.putText(frame,str(cnt),lm,font,fontScale,color,fontThickness) #lm is a tuple already, so dont need to index it 
            cnt=cnt+1
        
    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam',0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()
#junk

#mpDraw=self.mp.solutions.drawing_utils
        #drawSpecCircle=self.mpDraw.DrawingSpec(thickness=1,circle_radius=0,color=(255,0,0))
        #drawSPecLine=self.mpDraw.DrawingSpec(thickness=1,circle_radius=0,color=(0,0,255))
        #print(results) #prints <class 'mediapipe.python.solution_base.SolutionOutputs'>
        #print(results.multi_face_landmarks) #prints 468 datapoints as [,landmark { x: 2.37974072y: -1.80111456 z: -0.331219494],...]

    #if poseLM != []: #manipulating data from the pose class
    #    for index in [0,2,5,9,10]:
    #            cv2.circle(frame,poseLM[index],20,color,-1)
    #for face in faceLoc: #manipulating data from the face class
    #    cv2.rectangle(frame,face[0],face[1],color,fontThickness)
    #for hand,handType in zip(handsLM,handsType): #manipulating data from calling hand data
    #    if handType=='Right':
    #        lbl='Right'
    #    if handType=='Left':
    #        lbl='Left'
    #    cv2.putText(frame,lbl,hand[8],font,fontScale,color,fontThickness)        
    #cv2.putText(frame,str(indx),(int(lm.x*width),int(lm.y*height)),font,fontScale,color,fontThickness)
    #indx=indx+1
    #print(indx)
    #mpDraw.draw_landmarks(frame,faceLandmarks,self.mp.solutions.face_mesh.FACEMESH_CONTOURS,drawSpecCircle,drawSPecLine)
    #indx=0
    #drawSpecCircle=mpDraw.DrawingSpec(thickness=1,circle_radius=0,color=(255,0,0))
    #drawSPecLine=mpDraw.DrawingSpec(thickness=1,circle_radius=0,color=(0,0,255))


        #FaceMeshing=findFaceMesh.Marks(frame) #returns an array of 469 tuples
    #counterROI=1
    #counterROI2=counterROI+20
    #for tuplee in FaceMeshing[counterROI:counterROI2]:
    #    firstElement=tuplee[0]
    #    secondElement=tuplee[1]
    #    cv2.putText(frame,str(counterROI),(firstElement,secondElement),font,fontScale,color,fontThickness)
    #    counterROI=counterROI+1
    #    time.sleep(2)