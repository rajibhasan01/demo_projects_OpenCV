import cv2;
import mediapipe as mp;
import time;


count = 0;
face_orientation = 'front'

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

    def findFaceMesh(self, img, draw=True):
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
                    # if id == 1 or id == 93 or id == 323 or id == 175:
                    #   cv2.putText(img, str(id), (x, y), cv2.FONT_HERSHEY_PLAIN,
                    #             0.7, (0, 255, 0), 1);

        return img
      
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