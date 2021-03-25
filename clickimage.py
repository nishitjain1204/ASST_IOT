
import cv2
import time

#import beepy
frequency = 2800  # Set Frequency To 2500 Hertz
duration = 1500

face_cascade = cv2.CascadeClassifier('haarcascade_frontalcatface_extended.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
cap = cv2.VideoCapture(0)
count = 0
i = 0

while i == 0:
    _, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imshow("img", img)
   
    faces = face_cascade.detectMultiScale(gray, 1.1, 8)
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 3)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    for (ex, ey, ew, eh) in eyes:
        for (x, y, w, h) in faces:
            cv2.imshow('img', img)
            t = time.strftime("%Y-%m-%d_%H-%M-%S")
            print("Image " + t + "saved")
            file =  t + '.jpg'
            cv2.imwrite(file, img)
            count += 1

            if (x, y, w, h) in faces:
                cv2.destroyWindow("img")
                
                # beep(sound='ping')

                i += 1
                # print("haha")

