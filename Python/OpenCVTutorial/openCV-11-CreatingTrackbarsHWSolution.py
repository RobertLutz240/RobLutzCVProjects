import cv2
print(cv2.__version__)
def myCallBack1(val):
    global xPOS
    print(val)
    xPOS=val
def myCallBack2(val):
    global yPOS
    print(val)
    yPOS=val
def myCallBack3(val):
    width=val
    height=int(width*9/16)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
width=1280
height=720
xPOS=0
yPOS=0
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cv2.namedWindow('my TrackBars') #needed for 'my Trackbars
cv2.moveWindow('my TrackBars',width,0)
cv2.resizeWindow('my TrackBars', 400,150)
cv2.createTrackbar('xPOS','my TrackBars',0,2000,myCallBack1)
cv2.createTrackbar('yPOS','my TrackBars',0,2000,myCallBack2)
cv2.createTrackbar('width','my TrackBars',width,1920,myCallBack3) #trackbar variable, window name, min/max values, functin callback
while True:
    ignore, frame = cam.read()
    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam', xPOS,yPOS)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()