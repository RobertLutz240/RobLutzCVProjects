import cv2
print(cv2.__version__)

class mpHands:
    import mediapipe as mp
    def __init__(self,maxHands=2,tol1=int(.5),tol2=int(.5)):
        self.hands=self.mp.solutions.hands.Hands(False,maxHands,tol1,tol2)
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
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
findHands=mpHands(2)
while True:
    ignore,  frame = cam.read()
    frame=cv2.resize(frame,(width,height))
    handData,handsType=findHands.Marks(frame) #comma because we are catching two items from return
    #print(handData, handsType) handdata=[array of 20 landmark coordinates], handstype=[array of L,R hands]
    for hand,handType in zip(handData,handsType):
        if handType=='Right':
            handColor=(255,0,0)
        if handType=='Left':
            handColor=(0,0,255)
        for ind in [0,5,6,7,8]:
            cv2.circle(frame,hand[ind],25,handColor,3)
    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam',0,0)
    if cv2.waitKey(1) & 0xff ==ord('q'):
        break
cam.release()