from imutils import paths
import face_recognition
import pickle
import cv2
import os
 

def face_encoder(path):
#get paths of each file in folder named Images
#Images here contains my data(folders of various persons)
    imagePaths = list(paths.list_images(path))
    knownEncodings = []
    knownNames = []

    for (i, imagePath) in enumerate(imagePaths):
        # extract the person name from the image path
        name = imagePath.split(os.path.sep)[-2]
        # print(name)
        try:
            image = cv2.imread(imagePath)
            # print('-------------------------------------------------------------------------------------------------------')
            # print(imagePath)
            # print(image.shape)
            
            # image = cv2.resize(image,(0,0),None,0.25,0.25)

            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            #Use Face_recognition to locate faces
            boxes = face_recognition.face_locations(rgb,model='hog')
            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, boxes)
            # loop over the encodings
            for encoding in encodings:
                knownEncodings.append(encoding)
                knownNames.append(name)
        except Exception as e:
            print(e)

            print('invalid image')
    #save emcodings along with their names in dictionary data
    data = {"encodings": knownEncodings, "names": knownNames}
    return data
    
    #use pickle to save data into a file for later use

    # with open('face_enc','wb') as fp:
    #     # print(pickle.dumps(data))
    #     fp.write(pickle.dumps(data))
    # # f = open("face_enc", "wb")
    # f.write(pickle.dumps(data))
    # f.close()


