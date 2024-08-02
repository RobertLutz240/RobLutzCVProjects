import cv2
import face_recognition as FR
font=cv2.FONT_HERSHEY_SIMPLEX
width=640
height=360
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
 
paulFace=FR.load_image_file('C:/Users/nedm5/Documents/PythonVE/demoImages/known/Paul McWhorter.jpg') #loads the image
faceLoc=FR.face_locations(paulFace)[0] #sets the index of the face found in the image
paulFaceEncode=FR.face_encodings(paulFace)[0] #encodes the face from the image
 
gavFace=FR.load_image_file('C:/Users/nedm5/Documents/PythonVE/demoImages/known/Anthony Fauci.jpg')
faceLoc=FR.face_locations(gavFace)[0]
gavFaceEncode=FR.face_encodings(gavFace)[0]

robbyFace=FR.load_image_file('C:/Users/nedm5/Documents/PythonVE/demoImages/known/robby.jpg') #loads the image
faceLoc=FR.face_locations(robbyFace)[0] #sets the index of the face found in the image
robbyFaceEncode=FR.face_encodings(robbyFace)[0] #encodes the face from the image
 
knownEncodings=[paulFaceEncode,gavFaceEncode,robbyFaceEncode] #makes an array of known encodings
names=['Paul McWhorter','Anthony Fauci','robby'] #makes of array of names to match 
 
while True:
    ignore,  unknownFace = cam.read()
 
    unknownFaceRGB=cv2.cvtColor(unknownFace,cv2.COLOR_RGB2BGR) #we need to convert the camera feed to BGR so opencv can display it
    faceLocations=FR.face_locations(unknownFaceRGB) #create an array of faces in the camera feed
    unknownEncodings=FR.face_encodings(unknownFaceRGB,faceLocations) #encodes every face in the camera feed, using the location of all the faces

    for faceLocation,unknownEncoding in zip(faceLocations,unknownEncodings): #like a zipper, zips an index of facelocation and unknown encoding to the corresponding index in facelocations and unknown encodings
        top,right,bottom,left=faceLocation #catch the coodinates of the face locations
        print(faceLocation) 
        cv2.rectangle(unknownFace,(left,top),(right,bottom),(255,0,0),3) #draw a box in the camera feed using face location
        name='Unknown Person' #name to write if no 'known name' is found
        matches=FR.compare_faces(knownEncodings,unknownEncoding)
        print(matches) #FR.compare_faces returns true or false
        if True in matches: #if the image contains a match, loop to write a box with name
            matchIndex=matches.index(True) #sets a variabe to the number of the index that is true
            print(matchIndex) #prints the index. in this case, 0=paul,1=anthony fauci,2=robby
            print(names[matchIndex])#prints the string in the array "names" @ matchindex
            name=names[matchIndex] #sets a string (which by default we've said is unknown name) to write the name from names array
        cv2.putText(unknownFace,name,(left,top),font,.75,(0,0,255),2) #places text at the top of the box corresponding to name
    
    
    robbyFaceSmall=cv2.resize(robbyFace,(width,height)) #resize 4k image of me to a specified size
    robbyFaceSmall=cv2.cvtColor(robbyFaceSmall,cv2.COLOR_RGB2BGR)# converts BGR JPG of me to CV2's expected BGR
    cv2.imshow('my jpg', robbyFaceSmall)  #create a window with the resized image
    cv2.moveWindow('my jpg',width,0) #move window with my image
    cv2.imshow('My Faces',unknownFace)
    if cv2.waitKey(1) & 0xff ==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()