import os #library for navigating operating system
import cv2
import face_recognition as FR
print(cv2.__version__)
imageDir='C:/Users/nedm5/Documents/PythonVE/demoImages/known' #set the starting root directory
for root,dirs,files, in os.walk(imageDir): #loop that moves though the root, folders, and files.
    print('my working folder (root)', root)
    print('dirs in root', dirs)
    print('files in root', files)
    for file in files:
        print('your guy is', file)
        fullFilePath=os.path.join(root,file)#to automate file location we concatenate the imageDir from walk with the file name.
        print(fullFilePath)
        name=os.path.splitext(file)[0] #returns an array of the first part of the file name and the extension
        print(name)
        myPicture=FR.load_image_file(fullFilePath) #path to root+file loads the image
        myPicture=cv2.cvtColor(myPicture,cv2.COLOR_RGB2BGR)
        cv2.imshow(name,myPicture)
        cv2.moveWindow(name,0,0)
        cv2.waitKey(2500)
        cv2.destroyAllWindows()