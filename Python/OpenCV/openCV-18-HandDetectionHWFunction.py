import cv2
print(cv2.__version__)
import mediapipe as mp

hands=mp.solutions.hands.Hands(False,2,int(.5),int(.5)) #hands is a variable address
mpDraw=mp.solutions.drawing_utils

def parseLandmarks(frame): #this is a function
    myHands=[]
    frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results=hands.process(frameRGB)
    if results.multi_hand_landmarks !=None:
        for handLandMarks in results.multi_hand_landmarks:
            myHand=[]
            for landmark in handLandMarks.landmark:
                myHand.append((int(landmark.x*width),int(landmark.y*height)))
            myHands.append(myHand)
    return myHands

# lookForLandmarks=mp.solutions.hands.Hands(False,2,int(.5),int(.5)).process(frameRGB)
# lookForLandmarks=mp.solutions.hands.Hands(False,2,int(.5),int(.5)).multi_hand_landmarks

width=1280
height=720
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
while True:
    ignore, frame = cam.read()
    myHands=parseLandmarks(frame)
    for hand in myHands:
        for dig in [4,8,12,16,20]:
            cv2.circle(frame,hand[dig],25,(0,0,255),3)
    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam', 0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()