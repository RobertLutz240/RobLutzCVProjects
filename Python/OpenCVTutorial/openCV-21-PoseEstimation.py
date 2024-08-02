import cv2
print(cv2.__version__)
import mediapipe as mp
width=1280
height=720
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

pose=mp.solutions.pose.Pose(False,0,True,True,True,int(0.5),int(0.5)) #static image mode, model complexity(0,1,2),smooth landmarks,enable segmentiation, min detection confidence, max detection confidence
mpDraw=mp.solutions.drawing_utils
circleRadius=10
circleColor=(0,0,255)
circleThickness=4
eyeColor=(255,0,0)
eyeRadius=3
eyeThickness=-1
while True:
    ignore, frame = cam.read()
    frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results=pose.process(frameRGB)
    landMarks=[]
    if results.pose_landmarks != None:
        #mpDraw.draw_landmarks(frame,results.pose_landmarks,mp.solutions.pose.POSE_CONNECTIONS)
        for lm in results.pose_landmarks.landmark:
            print(lm.x,lm.y)
            landMarks.append((int(lm.x*width),int(lm.y*height)))
        cv2.circle(frame,landMarks[0],circleRadius,circleColor,circleThickness)
        cv2.circle(frame,landMarks[2],circleRadius,circleColor,circleThickness)
        cv2.circle(frame,landMarks[5],circleRadius,circleColor,circleThickness)
    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam', 0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()