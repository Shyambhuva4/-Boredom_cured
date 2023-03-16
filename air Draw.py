import cv2
import mediapipe as mp
import numpy as np
import time
import handTrackingModule as htm
import os

brushThickness=15

xp,yp=0,0
canvas=np.zeros((720,1280,3),np.uint8)

wCam,hCam=1280,720
drawColor=(255,0,255)

cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

detector=htm.handdetector(detectionCon=0.8)
while True:
    success, img =cap.read()
    img=cv2.flip(img,1)

    img=detector.findHands(img)
    lmlist=detector.Position(img,draw=False)

    if len(lmlist)!=0:

        x1,y1=lmlist[8][1:]
        x2, y2 = lmlist[12][1:]

        fingers=detector.fingersup()
        #print(fingers)

        if fingers[1] and fingers[2]:
            xp,yp=0,0
            if y1<125:
                if 250<x1<450:
                    drawColor=(255,0,255)
                elif 550<x1<750:
                    drawColor=(100,123,25)
                elif 800<x1<950:
                    drawColor=(0,255,0)
                elif 1050 <x1< 1200:
                    drawColor=(0,0,0)
            cv2.rectangle(img,(x1,y1-25),(x2,y2+25),drawColor,cv2.FILLED)



        if fingers[1] and fingers[2]==False:


            if xp==0 and yp==0:
                xp,yp=x1,y1

            if drawColor==(0,0.0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, 400)
                cv2.line(canvas, (xp, yp), (x1, y1), drawColor, 400)
                cv2.circle(img,(x1,x2),50,drawColor,cv2.FILLED)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(canvas, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            xp,yp=x1,y1

    imggray=cv2.cvtColor(canvas,cv2.COLOR_BGR2GRAY)
    _, imgInv=cv2.threshold(imggray,50,255,cv2.THRESH_BINARY_INV)
    imgInv=cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img=cv2.bitwise_and(img,imgInv)
    img=cv2.bitwise_or(img,canvas)

    cv2.circle(img,(350,100),75,(255,0,255),cv2.FILLED)
    cv2.circle(img, (650, 100), 75, (100,123,25), cv2.FILLED)
    cv2.circle(img, (900, 100), 75, (0, 255, 0), cv2.FILLED)
    cv2.circle(img, (1100, 100), 75, (0, 0, 0), cv2.FILLED)
    cv2.imshow("image", img)
    cv2.imshow("Canvas",canvas)
    cv2.waitKey(1)

    if cv2.waitKey(10) == ord('q'):
             break