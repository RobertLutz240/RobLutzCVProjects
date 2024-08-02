import cv2
print(cv2.__version__)
class mpHands:
    import mediapipe as mp
    def __init__(self,maxHands=2,tol1=int(0.5),tol2=int(0.5)):
        self.hands=self.mp.solutions.hands.Hands(False,maxHands,tol1,tol2)
        print("hello")
    def Marks(self,frame):
        myHands=[]
        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=self.hands.process(frameRGB)
        if results.multi_hand_landmarks != None:
            for handLandMarks in results.multi_hand_landmarks:
                myHand=[]
                for landmark in handLandMarks.landmark:
                    myHand.append((int(landmark.x*width),int(landmark.y*height)))
                myHands.append(myHand)
        return myHands
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
findHands=mpHands(1)
paddleWidth=125
paddleHeight=25
paddleColor=(0,255,0)
paddleROIBoundary=[0,0,0,0]
while True:
    ignore, frame = cam.read()
    #frame=cv2.flip(frame,1)
    handData=findHands.Marks(frame)
    for hand in handData:
        cv2.rectangle(frame,(int(hand[8][0]-paddleWidth/2),0),(int(hand[8][0]+paddleWidth/2),paddleHeight),paddleColor,-1) #8 is the index finger. zero is the index of the tuple returned at the index finger.
       #rectangles go from (upper left point,bottom right point)
        paddleROIBoundary=[(int(hand[8][0]-paddleWidth/2)),(int(hand[8][0]+paddleWidth/2)),0,paddleHeight]
        #print(paddleROIBoundary)
    cv2.circle(frame,(xPOS,yPOS),30,(0,0,255),2)
    xPOS=xPOS+slopeX
    yPOS=yPOS+slopeY
    if yPOS >= height-30: #bounce off floor
        slopeY=slopeY*-1
    if xPOS <= 30 or xPOS >= width-30: #bounce off walls
        slopeX=slopeX*-1
    if yPOS <= 30: #lose life and reset
        xPOS=int(width/2)
        yPOS=int(height/2)
        lives=lives-1
    if xPOS>int(paddleROIBoundary[0]-30) and xPOS<int(paddleROIBoundary[1]+30) and yPOS<int(paddleROIBoundary[3]+30):
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