import face_recognition
import imutils
import pickle
import time
import cv2
import os
 
def face_recognizer():
    #find path of xml file containing haarcascade file 
    print(os.path.dirname(cv2.__file__))
    cascPathface ="haarcascade_frontalcatface_extended.xml"
    # load the harcaascade in the cascade classifier
    faceCascade = cv2.CascadeClassifier(cascPathface)
    # load the known faces and embeddings saved in last file
    try:
        data = pickle.loads(open('face_enc', "rb").read())
    except  EOFError as e:
        pass
    
    print("Streaming started")
    video_capture = cv2.VideoCapture(0)
    

    # loop over frames from the video file stream
    while True:
        key = cv2.waitKey(1) & 0xFF
        # grab the frame from the threaded video stream
        ret, frame = video_capture.read()
        frame=cv2.rotate(frame,cv2.ROTATE_180)

       

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
       
        faces = faceCascade.detectMultiScale(gray,
                                            scaleFactor=1.1,
                                            minNeighbors=5,
                                            minSize=(60, 60),
                                            flags=cv2.CASCADE_SCALE_IMAGE)
    
        # convert the input frame from BGR to RGB 
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # the facial embeddings for face in input
        encodings = face_recognition.face_encodings(rgb)
        names = []
        # loop over the facial embeddings incase
        # we have multiple embeddings for multiple fcaes
        for encoding in encodings:
        #Compare encodings with encodings in data["encodings"]
        #Matches contain array with boolean values and True for the embeddings it matches closely
        #and False for rest
            matches = face_recognition.compare_faces(data["encodings"],
            encoding)
            #set name =inknown if no encoding matches
            name = "Unknown"
            # check to see if we have found a match
            if True in matches:
                #Find positions at which we get True and store them
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for i in matchedIdxs:
                    #Check the names at respective indexes we stored in matchedIdxs
                    name = data["names"][i]
                    #increase count for the name we got
                    counts[name] = counts.get(name, 0) + 1
                #set name which has highest count
                name = max(counts, key=counts.get)
    
    
            # update the list of names
            names.append(name)
            # loop over the recognized faces
        # for ((x, y, w, h), name) in zip(faces, names):
        #         # rescale the face coordinates
        #         # draw the predicted face name on the image
        #         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #         cv2.putText(frame, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
        #         0.75, (0, 255, 0), 2)
        # cv2.imshow("Frame", frame)

        time.sleep(10)
        
        if len(names)==1:
            if 'Unknown' in names:
                return 'unknown',frame
            else:
                # print(names[0])
                person = names[0]
                person=person[0:4]+' '+person[4:8]+' '+person[8:]
                video_capture.release()
                cv2.destroyAllWindows()
                print('in function: ',person)
                return person,frame
                
                break
           
        elif len(names)>1:
            print('more than one face')
            video_capture.release()
            cv2.destroyAllWindows()
            return 'unknown',frame
        else:
            if 'unknown' in names:
                video_capture.release()
                cv2.destroyAllWindows()
                return 'unknown',frame
                
                
       

            
     
   


