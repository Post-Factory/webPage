from flask import Flask, render_template, Response
import os
from importlib import import_module
import cv2
import numpy as np
import time
import datetime
import sys

# if os.environ.get('CAMERA'):
#     camera = import_module('camera_' + os.environ['CAMERA']).Camera
#     print("if")
# else:
#     from camera import Camera
#     print("else")

app = Flask(__name__)

camera = cv2.VideoCapture(0)

def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if (not success):
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                   # concat frame one by one and show result

@app.route("/")
def main() :
    return render_template('main_index.html')

@app.route("/first")
def first() :
    return render_template('first_index.html')

@app.route("/second")
def second() :
    return render_template('second_index.html')

@app.route("/third")
def third() :
    """Video streaming home page."""
    return render_template('camera.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')