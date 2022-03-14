import cv2
from flask import Flask, render_template, render_template_string, Response

import mediapipe as mp;
import time;
import FaceMeshModule as fm;
import face_question as fq;
import os;



app = Flask(__name__)
video_capture = cv2.VideoCapture(0)
detector = fm.FaceMeshDetector(max_num_faces=1);

def gen(): 
    fq.generate_status();
    while True:
        ret, image = video_capture.read()
        image = cv2.flip(image,1);
        image = detector.findFaceMesh(image, False);
        image, face_orientation = detector.find_Orientation(image, False);
        # print(face_orientation)
        # if len(face)!= 0:
        #     # print(face[0]);
    
        # Generating new question
        new_question = fq.generate_qstn(image);
    
         # Matching buffer ans with current question
        fq.match_q_a(face_orientation);
    
        cv2.imwrite('t.jpg', image)
        yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')
    video_capture.release()


def gen_rerun(value): 
    
    fq.generate_status();
    while True:
        ret, image = video_capture.read()
        image = cv2.flip(image,1);
        image = detector.findFaceMesh(image, False);
        image, face_orientation = detector.find_Orientation(image, False);
        # print(face_orientation)
        # if len(face)!= 0:
        #     # print(face[0]);
    
        # Generating new question
        new_question = fq.generate_qstn(image, value);
    
         # Matching buffer ans with current question
        fq.match_q_a(face_orientation);
    
        cv2.imwrite('t.jpg', image)
        yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')
    video_capture.release()

@app.route('/')
def index():
    """Video streaming"""
    #return render_template('index.html')
    return render_template_string('''<html>
<head>
    <title>Video Streaming </title>
    <style>
        .container{
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100vh;
            background-color: beige;
            color: black;
            text-align: center;
        }
       
        .button {
            background-image: linear-gradient(#0dccea, #0d70ea);
            border: 0;
            border-radius: 4px;
            box-shadow: rgba(0, 0, 0, .3) 0 5px 15px;
            box-sizing: border-box;
            color: #fff;
            cursor: pointer;
            font-family: Montserrat,sans-serif;
            font-size: .9em;
            margin-top: 50px;
            padding: 10px 35px;
            text-align: center;
            user-select: none;
            -webkit-user-select: none;
            touch-action: manipulation;
            }
    </style>
</head>
<body>
    
    <div class="container">
    <a href="/"><input type="button" value="rerun"></a>
        <h1>Liveliness Checking</h1>
        <canvas id="canvas" width="640px" height="480px"></canvas>
    </div>

<script >

    
    var ctx = document.getElementById("canvas").getContext('2d');
    
    var img = new Image();
    img.src = "{{ url_for('video_feed') }}";

    // need only for static image
    //img.onload = function(){   
    //    ctx.drawImage(img, 0, 0);
    //};

    // need only for animated image
    function refreshCanvas(){
        ctx.drawImage(img, 0, 0);
    };
    window.setInterval("refreshCanvas()", 10);

</script>
</body>
</html>''')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                mimetype='multipart/x-mixed-replace; boundary=frame')
    

@app.route('/your_flask_funtion')
def rerun():
    # os.system("python /home/rajibhasan/Desktop/Demo_Projects/face_mask/web_page/web.py")
    return render_template_string('''<html>
<head>
    <title>Video Streaming </title>
    <style>
        .container{
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100vh;
            background-color: beige;
            color: black;
            text-align: center;
        }
       
        .button {
            background-image: linear-gradient(#0dccea, #0d70ea);
            border: 0;
            border-radius: 4px;
            box-shadow: rgba(0, 0, 0, .3) 0 5px 15px;
            box-sizing: border-box;
            color: #fff;
            cursor: pointer;
            font-family: Montserrat,sans-serif;
            font-size: .9em;
            margin-top: 50px;
            padding: 10px 35px;
            text-align: center;
            user-select: none;
            -webkit-user-select: none;
            touch-action: manipulation;
            }
    </style>
</head>
<body>
    
    <div class="container">
    <a href="/your_flask_funtion"><input type="button" value="rerun"></a>
        <h1>Liveliness Checking</h1>
        <canvas id="canvas" width="640px" height="480px"></canvas>
    </div>

<script >

    
    var ctx = document.getElementById("canvas").getContext('2d');
    
    var img = new Image();
    img.src = "{{ url_for('video_feed_rerun') }}";

    // need only for static image
    //img.onload = function(){   
    //    ctx.drawImage(img, 0, 0);
    //};

    // need only for animated image
    function refreshCanvas(){
        ctx.drawImage(img, 0, 0);
    };
    window.setInterval("refreshCanvas()", 10);

</script>
</body>
</html>''')
    

if __name__ == '__main__':
    app.run()