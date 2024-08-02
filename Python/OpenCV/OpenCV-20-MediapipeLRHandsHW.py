import cv2
print(cv2.__version__)
class mpHands:
    import mediapipe as mp
    def __init__(self,maxHands=2,tol1=int(0.5),tol2=int(0.5)):
        self.hands=self.mp.solutions.hands.Hands(False,maxHands,tol1,tol2)
        print("hello")
    def Marks(self,frame):
        myHands=[]
        handsType=[]
        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=self.hands.process(frameRGB)
        if results.multi_hand_landmarks != None:
            #print(results.multi_handedness)
            for hand in results.multi_handedness:
                handType=hand.classification[0].label #this parses the hand type (L/R) from the hand
                handsType.append(handType) # this inserts the hand type for each hand
            for handLandMarks in results.multi_hand_landmarks:
                myHand=[]
                for landMark in handLandMarks.landmark:
                    myHand.append((int(landMark.x*width),int(landMark.y*height)))
                myHands.append(myHand)
        return myHands,handsType #we now throw two arrays. one with an array of landmarks and the other with whether its L or R

width=1280
height=720
xPOS=int(width/2)
yPOS=int(height/2)
slopeX=-2
slopeY=-2
lives=5
points=0
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
findHands=mpHands(2)
paddleWidth=125
paddleHeight=25
paddleColorR=(255,0,0)
paddleColorB=(0,0,255)
paddle1ROIBoundary=[0,0,0,0]
paddle2ROIBoundary=[0,0,0,0]
while True:
    ignore, frame = cam.read()
    #frame=cv2.flip(frame,1)
    handData,handsType=findHands.Marks(frame) #comma because we are catching two items from return
    for hand,handType in zip(handData,handsType):
        if handType=='Right':
            handColor=(255,0,0)
            cv2.rectangle(frame,(int(hand[8][0]-paddleWidth/2),height),(int(hand[8][0]+paddleWidth/2),height-paddleHeight),paddleColorR,-1)
            paddle1ROIBoundary=[(int(hand[8][0]-paddleWidth/2)),(int(hand[8][0]+paddleWidth/2)),height,height-paddleHeight]
        if handType=='Left':
            handColor=(0,0,255)
            cv2.rectangle(frame,(int(hand[8][0]-paddleWidth/2),0),(int(hand[8][0]+paddleWidth/2),paddleHeight),paddleColorB,-1)
            paddle2ROIBoundary=[(int(hand[8][0]-paddleWidth/2)),(int(hand[8][0]+paddleWidth/2)),0,paddleHeight]
        for ind in [8]:
            cv2.circle(frame,hand[ind],25,handColor,2)
        #for hand in handData:
             #8 is the index finger. zero is the index of the tuple returned at the index finger.
       #rectangles go from (upper left point,bottom right point)
            
            
        #print(paddleROIBoundary)
    cv2.circle(frame,(xPOS,yPOS),30,(0,255,0),-1)
    xPOS=xPOS+slopeX
    yPOS=yPOS+slopeY
    if yPOS >= height-30: #bounce off floor
        xPOS=int(width/2)
        yPOS=int(height/2)
        lives=lives-1
    if xPOS <= 30 or xPOS >= width-30: #bounce off walls
        slopeX=slopeX*-1
    if yPOS <= 30: #lose life and reset
        xPOS=int(width/2)
        yPOS=int(height/2)
        lives=lives-1
    if xPOS>int(paddle1ROIBoundary[0]-30) and xPOS<int(paddle1ROIBoundary[1]+30) and yPOS>int(paddle1ROIBoundary[3]-30) or xPOS>int(paddle2ROIBoundary[0]-30) and xPOS<int(paddle2ROIBoundary[1]+30) and yPOS<int(paddle2ROIBoundary[3]+30):
        slopeY=slopeY*-1
        points=points+1
        slopeX=slopeX+int(slopeX*0.25)
        slopeY=slopeY+int(slopeY*0.25)
        
    
    cv2.putText(frame, str(lives)+"Lives",(int(width*0.75),int(height*0.075)),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),1)
    cv2.putText(frame, str(points)+"points",(int(width*0.25),int(height*0.075)),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),1)
    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam', 0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()







while True:
    ignore,  frame = cam.read()
    frame=cv2.resize(frame,(width,height))
    handData,handsType=findHands.Marks(frame) #comma because we are catching two items from return
    #print(handData, handsType) handdata=[array of 20 landmark coordinates], handstype=[array of L,R hands]

