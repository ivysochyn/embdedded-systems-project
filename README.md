# Embedded systems project
This repository contains realisation of my face recognition app for 'Embedded Systems' laboratory in Poznan University of Technology.

## Face recognition
The idea is to have system which will check the attendance of people. If person is in the `allowed-persons` database, then write `date + time` + `name` into database.

### How to run
In order to run the demo, first create `images` folder in the same path the demo is, and put there images of faces you want to recognize.
Run the program using:
```
./camera.py
```

### Requirements
* OpenCV
* dlib <= 19.15.0
* face_recognition
* numpy
* pysqlite3
