import cv2
print(cv2.__version__)
def myCallBack1(val): #val catches the incoming value on the trackbar object,
    global xPOS
    print("xPOS= "+str(val))
    xPOS=val
def myCallBack2(val): #val catches the incoming value on the trackbar object,
    global yPOS
    print("xPOS= "+str(val))
    yPOS=val
def myCallBack3(val):
    global myRad
    print("myRad= "+str(val))
    myRad=val
def myCallBack4(val):
    global myThick
    print("myRad= "+str(val))
    myThick=val
width=1280
height=720
myRad=25
myThick=1
xPOS=int(width/2)
yPOS=int(height/2)
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'M','J','P','G'))
cv2.namedWindow('myTrackbars')
cv2.resizeWindow('myTrackbars',400,300)
cv2.moveWindow('myTrackbars',width,0)
cv2.createTrackbar('xPOS','myTrackbars',xPOS,1920,myCallBack1) #trackbar name, window name, value range, function callback
cv2.createTrackbar('yPOS','myTrackbars',yPOS,1080,myCallBack2) #trackbar name, window name, value range, function callback
cv2.createTrackbar('radius','myTrackbars',myRad,1080,myCallBack3) #trackbar name, window name, value range, function callback
cv2.createTrackbar('thickness','myTrackbars',myThick,7,myCallBack4) #trackbar name, window name, value range, function callback
while True:
    ignore, frame = cam.read()
    if myThick==0:
        myThick=(-1)
    cv2.circle(frame,(xPOS,yPOS),myRad,(255,0,0),myThick)  
    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam', 0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()