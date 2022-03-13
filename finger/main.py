import cv2
import time
import os
import HandTrackingModule as htm
import question as qs


# Camera Opening
wCam, hCam = 640, 480;
cap = cv2.VideoCapture(0);

detector = htm.handDetector(detectionCon=0.75);
tipIds = [4, 8, 12, 16, 20];

while True:
    success, img = cap.read();
    img = cv2.flip(img, 1);
    img = detector.findHands(img, draw=True);
    lmList = detector.findPosition(img, handNo=0, draw=True);

    # Generating new question
    new_question = qs.generate_qstn(img);

    if len(lmList) != 0:
        fingers = []

        # Thumb Finger Count
        # if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
        #     fingers.append(1)
        # else:
        #     fingers.append(0)

        # 4 Fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        totalFingers = fingers.count(1)

        # Matching buffer ans with current question
        qs.match_q_a(img, totalFingers, new_question);

    
    cv2.imshow("Image", img)
    cv2.waitKey(10)