import cv2
import numpy as np
#generate a blank data aray
#rows will hold saturation values(0-255), hues, 3 values 
#np.zeros [rows(height),columns(width)]
x=np.zeros([256,720,3],dtype=np.uint8)
y=np.zeros([256,720,3],dtype=np.uint8)
for row in range(0,256,1): #for loop that moves from 0 to 256 in steps of one
    for column in range(0,720,1): #zero counts as a spot so its counting 180
        x[row,column]=(int(column/4),row,255) #to modify the array one pixel at a time [ROW,COLUMN!!!]
        y[row,column]=(int(column/4),255,row) #to modify the array one pixel at a time [ROW,COLUMN!!!]
x=cv2.cvtColor(x,cv2.COLOR_HSV2BGR)
y=cv2.cvtColor(y,cv2.COLOR_HSV2BGR)
while True:
    #display x arrray
    cv2.imshow('my HSV2',x)
    cv2.moveWindow('my HSV2',0,0)
    cv2.imshow('my HSV',y)
    cv2.moveWindow('my HSV',720,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cv2.destroyAllWindows()