import face_recognition
import cv2
import os
import numpy as np
import  datetime

path = 'Entities_Images'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
     curImg = cv2.imread(f'{path}/{cl}')
     images.append(curImg)
     classNames.append(os.path.splitext(cl)[0])
# print(images)
print(classNames)


def findEncodings(images):
     encodeList = []
     for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
     return encodeList


encodeListKnown = findEncodings(images)
# print(encodeListKnown)

imgS = face_recognition.load_image_file("suraj.jpg")
print(type(imgS))
face_test = face_recognition.face_locations(imgS)
encode_test = face_recognition.face_encodings(imgS)
# print(encode_test)
print(len(encodeListKnown))
face_dis_list=[]
for i in encodeListKnown:
    match = face_recognition.compare_faces(i,encode_test)
    face_dis = face_recognition.face_distance(i,encode_test)
    face_dis_list.append(face_dis)
print(face_dis_list)
index = np.argmin(face_dis_list)
Id = classNames[index]
print(index)
print(Id)












