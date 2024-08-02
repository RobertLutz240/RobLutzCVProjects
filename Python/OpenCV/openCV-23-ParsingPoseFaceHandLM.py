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


#faceMesh=mp.solutions.face_mesh.FaceMesh(False,1,False,int(.5),int(.5)) #object we use to computate our facemesh (static,number of face,tacking)
faceMesh=mp.solutions.face_mesh.FaceMesh(False,1,True,int(.5),int(.5))
mpDraw=mp.solutions.drawing_utils

drawSpecCircle=mpDraw.DrawingSpec(thickness=1,circle_radius=0,color=(255,0,0))
drawSPecLine=mpDraw.DrawingSpec(thickness=1,circle_radius=0,color=(0,0,255))

font=cv2.FONT_HERSHEY_SIMPLEX
fontSize=0.5
fontColor=(0,255,255)
fontThickness=1
while True:
    ignore, frame = cam.read()
    frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results=faceMesh.process(frameRGB)
    #print(results) #prints <class 'mediapipe.python.solution_base.SolutionOutputs'>
    #print(results.multi_face_landmarks) #prints 468 datapoints as [,landmark { x: 2.37974072y: -1.80111456 z: -0.331219494],...]
    if results.multi_face_landmarks != None:
        for faceLandmarks in results.multi_face_landmarks:
            mpDraw.draw_landmarks(frame,faceLandmarks,mp.solutions.face_mesh.FACEMESH_CONTOURS,drawSpecCircle,drawSPecLine)
            indx=0
            for lm in faceLandmarks.landmark:
                cv2.putText(frame,str(indx),(int(lm.x*width),int(lm.y*height)),font,fontSize,fontColor,fontThickness)
                indx=indx+1
                print(indx)
    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam', 0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()