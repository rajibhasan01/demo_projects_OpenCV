
from flask import Flask
from flask import render_template
from flask import Response

import cv2

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)