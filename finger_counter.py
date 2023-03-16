import cv2
import mediapipe as mp
import numpy as np
import time
import handTrackingModule as htm
import os
wCam,hCam=640,480


cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
ptime =0
folderpath = "finger_images"
mylist = os.listdir(folderpath)
overlaylist=[]
for impath in mylist:
    image=cv2.imread(f'{folderpath}/{impath}')
    overlaylist.append(image)

detector=htm.handdetector(detectionCon=0.7)

tipid= [4,8,12,16,20]

while True:
    succes, img =cap.read()
    img=detector.findHands(img)
    lmlist=detector.Position(img,draw=False)

    if len(lmlist) !=0:
        fingers=[]
        #for thumb
        if lmlist[tipid[0]][1] < lmlist[tipid[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        #for fingers
        for id in range(1,5):
            if lmlist[tipid[id]][2] < lmlist[tipid[id]-2][2]:
               fingers.append(1)
            else:
                fingers.append(0)
        #print(fingers)


        totalfingers=fingers.count(1)
        #print(totalfingers)


        h,w,c= overlaylist[totalfingers-1].shape
        img[0:h,0:w]= overlaylist[totalfingers-1]
    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    cv2.putText(img, f'FPS:{int(fps)}', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 400, 32), 2)
    cv2.imshow("Tracker", img)
    cv2.waitKey(1)
    if cv2.waitKey(10) == ord('q'):
             break