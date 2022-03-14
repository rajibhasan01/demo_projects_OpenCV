from turtle import distance
import cv2;
import mediapipe as mp;
import time;
import numpy as np

count = 0;
constant_value = 30;
face_orientation = 'front';
distance = None;

class FaceMeshDetector(): 
    def __init__(self,
               static_image_mode=False,
               max_num_faces=1,
               refine_landmarks=False,
               min_detection_confidence=0.5,
               min_tracking_confidence=0.5):

        self.staticMode = static_image_mode;
        self.maxFaces = max_num_faces;
        self.refine_landmarks = refine_landmarks;
        self.minDetectionCon = min_detection_confidence;
        self.minTrackCon = min_tracking_confidence;

        self.mpDraw = mp.solutions.drawing_utils;
        self.mpFaceMesh = mp.solutions.face_mesh;
        self.faceMesh = self.mpFaceMesh.FaceMesh(self.staticMode, self.maxFaces, self.refine_landmarks,
                                                 self.minDetectionCon, self.minTrackCon);
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=1, circle_radius=2);

    def findFace(self, img, draw=True):
        global constant_value;
        global distance;
        
        self.imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB);
        self.results = self.faceMesh.process(self.imgRGB);
        faces = [];
        if self.results.multi_face_landmarks:
            for faceLms in self.results.multi_face_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, faceLms, self.mpFaceMesh.FACEMESH_CONTOURS,
                                           self.drawSpec, self.drawSpec);

                for id,lm in enumerate(faceLms.landmark):
                    #print(lm)
                    ih, iw, ic = img.shape;
                    x,y = int(lm.x*iw), int(lm.y*ih);
                    
                    if id == 93:
                      x1 = x - constant_value;
                    if id == 10:
                      y1 = y - constant_value + 10;
                    
                    if id == 152:
                      y2 = y + constant_value -10;
                    if id == 454:
                      x2 = x + constant_value;
                      
                      img = cv2.rectangle(img, (x1 , y1 ), (x2 ,y2 ), (0,0,255), 2);
                      
                      # check face distance from camera
                      distance = check_face_distance(x1,y1, x2, y2)
                      
                      # cv2.putText(img, str("."), (x, y), cv2.FONT_HERSHEY_PLAIN,
                      #           1, (0, 0, 255), 5);
                      
                      # print("id-93 x_axis ", x);
                    # img = np.ones_like(img) * 255
                    img = cv2.rectangle(img, (150,80), (490,400), (0,255,0), 2);
                    
                    
                    # img = cv2.GaussianBlur(img,(3,3),0);    

        return img, distance;
      
    
    def findFaceMesh(self, img, draw=True):
        global constant_value;
        global distance;
        
        self.imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB);
        self.results = self.faceMesh.process(self.imgRGB);
        faces = [];
        if self.results.multi_face_landmarks:
            for faceLms in self.results.multi_face_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, faceLms, self.mpFaceMesh.FACEMESH_CONTOURS,
                                           self.drawSpec, self.drawSpec);

        return img;
    
      
    def find_Orientation(self, img):
      
      global count;
      global face_orientation;

      if self.results.multi_face_landmarks:
          for faceLms in self.results.multi_face_landmarks:
            
            if faceLms.landmark[1].x >= faceLms.landmark[323].x:
              face_orientation = "right";

            elif faceLms.landmark[1].x <= faceLms.landmark[93].x:
              face_orientation = "left";

            elif faceLms.landmark[134].y <= faceLms.landmark[127].y:
              face_orientation = "up";
              
            else:
              face_orientation = "font"
            
            
      return img, face_orientation;
              


# checking face distance
def check_face_distance(x1,y1, x2, y2):
  global face_distance;

  if x1 < 150 or y1 < 80 or x2 > 490 or y2 > 400:
    face_distance = 'zoom';
    
  else:
    if x1 - 150 > 100 or y1 - 80 > 80:
      face_distance = 'long';
    
    elif 490 - x2 > 100 or 400 - y2 > 80:
      face_distance = 'long';
      
    else:
      face_distance = 'ok';
      
  
  return face_distance;
      

def main():
    cap = cv2.VideoCapture(0);
    pTime = 0;
    detector = FaceMeshDetector(max_num_faces=1);
    
    while True:
        success, img = cap.read();
        img, face = detector.findFaceMesh(img);
        cTime = time.time();
        fps = 1 / (cTime - pTime);
        pTime = cTime;

        cv2.imshow("Image", img);
        cv2.waitKey(1);


if __name__ == "__main__":
    main();