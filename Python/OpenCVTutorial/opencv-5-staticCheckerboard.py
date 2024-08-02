import cv2
print(cv2.__version__)
import numpy as np
rowStart=0
rowEnd=50
colStart=0
colEnd=50
endCount = 0
while True:
    frame=np.zeros([1000,1000,3],dtype=np.uint8)
    frame[:,:]= 0,0,255
    while endCount < 300:
        
        frame[rowStart:rowEnd,colStart:colEnd]=0,0,0
        frame[rowStart+50:rowEnd+50,colStart+50:colEnd+50]=0,0,0
        rowStart=rowStart+100
        rowEnd=rowEnd+100
        if rowEnd >= 1000:
            if endCount % 2 == 0:
                colStart=colStart+100
                colEnd=colEnd+100
                rowStart=0
                rowEnd=50
                endCount=endCount+1
            else:
                colStart=colStart
                colEnd=colEnd
                rowStart=10
                rowEnd=10
                print(endCount)
                endCount=endCount+1
        endCount=endCount+1
        
        cv2.imshow('my window', frame)   
    if cv2.waitKey(1) & 0xff ==ord('q'):
        break