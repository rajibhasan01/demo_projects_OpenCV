import cv2;
import mediapipe as mp;
import time;
import FaceMeshModule as fm;
import face_question as fq;

cap = cv2.VideoCapture(0);
detector = fm.FaceMeshDetector(max_num_faces=1);
    
while True:
    success, img = cap.read();
    img = cv2.flip(img,1);
    img = detector.findFaceMesh(img);
    img, face_orientation = detector.find_Orientation(img);
    # print(face_orientation)
    # if len(face)!= 0:
    #     # print(face[0]);
    
    # Generating new question
    new_question = fq.generate_qstn(img);
    
    # Matching buffer ans with current question
    fq.match_q_a(face_orientation);
    # print("orientation", face_orientation);

    cv2.imshow("Image", img);
    cv2.waitKey(10);
