import cv2
print(cv2.__version__)

def myCallBack1(val): #val catches the incoming value on the trackbar object,
    global width
    print("width= "+str(val))
    width=val
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    height=width/9
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    #16:9
def myCallBack2(val): #val catches the incoming value on the trackbar object,
    global height
    print("height= "+str(val))
    height=val
    width=16/height
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
def myCallBack3(val):
    global anchorX
    print("anchorX= "+str(val))
    anchorX=val
def myCallBack4(val):
    global anchorY
    print("anchorY= "+str(val))
    anchorY=val
width=1280
height=720
anchorX=0
anchorY=0
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'M','J','P','G'))
cv2.namedWindow('myTrackbars')
cv2.resizeWindow('myTrackbars',400,300)
cv2.moveWindow('myTrackbars',width,0)
cv2.createTrackbar('width','myTrackbars',0,1280,myCallBack1)
cv2.createTrackbar('height','myTrackbars',0,720,myCallBack2)
cv2.createTrackbar('anchorX','myTrackbars',anchorX,1920,myCallBack3)
cv2.createTrackbar('anchorY','myTrackbars',anchorY,1920,myCallBack4)
while True:
    ignore, frame = cam.read()
    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam', anchorX,anchorY)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()


#create a trackbar the defines the size of the image
# hint: keep 16:9 ratio
# dont use resize, use cam.set
# assign values to cam.set from trackbars
#make a slider that moves the window anchor point up and down