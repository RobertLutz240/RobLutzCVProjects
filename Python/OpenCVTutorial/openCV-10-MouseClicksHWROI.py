import cv2
print(cv2.__version__)
evt=0 #seeding the program with evt value so program doesnt crash
width=1280
height=720
ROItrigger1=0
ROItrigger2=0
def mouseClick(event,xPOS,yPOS,flags,params): #these items in orange are all variables, can be named anything.
    global evt
    global pnt
    global pnt2
    global ROItrigger1
    global ROItrigger2
    if event==cv2.EVENT_LBUTTONDOWN:
        print('Mouse Event Was: ', event)
        print('At Position: ',xPOS,yPOS)
        evt=event
        pnt=(xPOS,yPOS)
        ROItrigger1=1
    if event==cv2.EVENT_LBUTTONUP:
        print('Mouse Event Was: ', event)
        print('At Position: ',xPOS,yPOS)
        evt=event
        pnt2=(xPOS,yPOS)
        ROItrigger2=1
    if event==cv2.EVENT_RBUTTONUP:
        print('RB Event Was: ', event)
        evt=event
        ROItrigger1=0
        ROItrigger2=0
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'M','J','P','G'))
cv2.namedWindow('my WEBcam') #creates a window so setMouseCallback doesn't crash
#cv2.namedWindow('PIP ROI') #creates a window so setMouseCallback doesn't crash
cv2.setMouseCallback('my WEBcam', mouseClick) #all this does is send the program to a function on mouseclick
while True:
    ignore, frame = cam.read()
    if evt==1 or evt == 4:
        cv2.circle(frame,pnt,25,(255,0,0),2)
    if evt ==4:
        cv2.circle(frame,pnt2,25,(0,0,255),2)
    if ROItrigger1 and ROItrigger2 ==1:
        frameROI=frame[pnt[1]:pnt2[1],pnt[0]:pnt2[0]]
        cv2.imshow("PIP ROI",frameROI)
        cv2.moveWindow('PIP ROI',width,0)
    if evt==5:
        cv2.destroyAllWindows()
        evt=0

    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam', 0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()



# Define a ROI using pnt LbuttonDown, and pnt LbuttonUP

#create a new window 
#frame=cv2.resize(frame,(int(width/columns),int(height/columns)))