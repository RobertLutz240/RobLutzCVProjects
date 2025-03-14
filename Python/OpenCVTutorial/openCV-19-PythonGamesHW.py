#make the game pong
#score counter
#as game goes on ball speed increases


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
slopeX=1
slopeY=1

cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
findHands=mpHands(2)
paddleWidth=125
paddleHeight=25
paddleColor=(0,255,0)
while True:
    ignore, frame = cam.read()
    #frame=cv2.flip(frame,1)
    handData=findHands.Marks(frame)
    for hand in handData:
        cv2.rectangle(frame,(int(hand[8][0]-paddleWidth/2),0),(int(hand[8][0]+paddleWidth/2),paddleHeight),paddleColor,-1) #8 is the index finger. zero is the index of the tuple returned at the index finger.
       #rectangles go from (upper left point,bottom right point)
    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam', 0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()