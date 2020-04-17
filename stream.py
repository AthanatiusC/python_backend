#
# stream.py
# Vision-Intelligent-Platform
#
# Created by Purwo Widodo on 09/01/2020.
# Copyright © 2019 Purwo Widodo. All rights reserved.
#

from flask import Flask, render_template, Response,request
import facerecog

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def generate(fr):
    while True:
        jpg_bytes = fr.jpg_bytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpg_bytes + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    cam_type = request.args.get('cam_type')
    ip_add = request.args.get('ip_add')
    username = request.args.get('username')
    password = request.args.get('password')
    id_camRTSP = request.args.get('id_cam')
    return Response(generate(facerecog.Recognition(cam_type,ip_add,username,password,id_camRTSP)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
