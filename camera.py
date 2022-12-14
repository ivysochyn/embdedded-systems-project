#!/usr/bin/python3

import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import database

path = "images"
images = []
classNames = []
myList = os.listdir(path)
for cls in myList:
    curImg = cv2.imread(f'{path}/{cls}')
    images.append(curImg)
    classNames.append(os.path.splitext(cls)[0])


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


processFrame = False
conn = database.create_connection("camera.db")
rectangles = list()
with conn:
    camera = 'Camera'
    cv2.namedWindow(camera, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(camera, cv2.WND_PROP_FULLSCREEN,
                          cv2.WINDOW_FULLSCREEN)
    database.create_table(conn, database.sql_create_attendance_table)
    encodeListKnown = findEncodings(images)
    capture = cv2.VideoCapture(0)
    while True:
        success, img = capture.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        if processFrame:
            rectangles = []
            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS,
                                                              facesCurFrame)

            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown,
                                                         encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown,
                                                         encodeFace)
                matchIndex = np.argmin(faceDis)
                if faceDis[matchIndex] < 0.5:
                    date = datetime.now()
                    day = date.strftime("%d/%m/%Y")
                    time = date.strftime("%H:%M")
                    name = classNames[matchIndex].upper()
                    data = (name, day, time)
                    if not(database.exists(conn, data)):
                        database.write_to_table(conn, (name, day, time))
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                    rectangles.append((name, x1, y1, x2, y2))
        key = cv2.waitKey(1)
        if key == ord("q"):
            break
        elif key == ord("p"):
            person_name = datetime.now().strftime('%d_%m_%Y_%H%M%S')
            person_name = f"images/{person_name}.jpg"
            cv2.imwrite(person_name, img)
        for rect in rectangles:
            name, x1, y1, x2, y2 = rect
            padding = 10
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, name, (x1, y1-padding), cv2.FONT_HERSHEY_COMPLEX,
                        1, (255, 255, 255), 1)
        processFrame = not processFrame
        cv2.imshow(camera, img)
