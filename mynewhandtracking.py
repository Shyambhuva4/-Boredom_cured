import cv2
import mediapipe as mp
import time
import handTrackingModule as htm


ptime = 0
ctime = 0
cap = cv2.VideoCapture(0)
detector=htm.handdetector()
while True:
    success, img = cap.read()
    img= detector.findHands(img)
    lmlist = detector.Position(img)
    if len(lmlist) != 0:
        print(lmlist[1])
    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 225), 3)
    cv2.imshow("Tracker", img)
    cv2.waitKey(1)
