import cv2
import mediapipe as mp
import time
import FaceMeshModule as fm

cap = cv2.VideoCapture(0)
pTime = 0
detector = fm.FaceMeshDetector(max_num_faces=1)
    
while True:
    success, img = cap.read();
    img = cv2.flip(img,1)
    img = detector.findFaceMesh(img)
    detector.find_Orientation(img)
    # if len(face)!= 0:
    #     # print(face[0])
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.imshow("Image", img)
    cv2.waitKey(1)
