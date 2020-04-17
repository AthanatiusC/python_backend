from flask import Flask, request, redirect, render_template, Response, jsonify
from datetime import datetime
import json
import re
import time

from modules.base.util import compare_faces, face_rec, find_facial_features, find_face_locations
from modules.crop import recognize

app = Flask(__name__)

UPLOAD_FOLDER = 'trash'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def gen(fr):
    while True:
        try:
            jpg_bytes = fr.get_jpg_bytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + jpg_bytes + b'\r\n\r\n')
        except:
            pass


@app.route('/crop')
def crop_image():
    return render_template('crop/index.html')


@app.route('/crop_feed')
def video_feed():
    # cam_type = request.args.get('cam_type', default=None, type=None)
    ip_addr = request.args.get('ip_addr', default=None, type=None)
    username = request.args.get('username', default=None, type=None)
    password = request.args.get('password', default=None, type=None)
    cam_path = request.args.get('cam_path', default=None, type=None)
    id_cam   = request.args.get('id_cam', default=None, type=None)
    return Response(gen(recognize.FaceRecog(ip_addr=ip_addr,
                                            username=username,
                                            password=password,
                                            cam_path=cam_path,
                                            id_cam=id_cam)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/facematch', methods=['POST', 'GET'])
def face_match():
    if request.method == 'POST':
        # check if the post request has the file part
        if ('file1' not in request.files) or ('file2' not in request.files):
            print('No file part')
            return redirect(request.url)

        file1 = request.files.get('file1')
        file2 = request.files.get('file2')
        # if user does not select file, browser also submit an empty part without filename
        if file1.filename == '' or file2.filename == '':
            print('No selected file')
            return redirect(request.url)

        if allowed_file(file1.filename) and allowed_file(file2.filename):
            ret = compare_faces(file1, file2)
            # convert numpy._bool of ret to bool for json.dumps
            resp_data = {"match": bool(ret)}
            return json.dumps(resp_data)

    # Return a demo page for GET request
    return render_template('facematch/index.html')


def print_request(request):
    # Print request url
    print(request.url)
    # print relative headers
    print('content-type: "%s"' % request.headers.get('content-type'))
    print('content-length: %s' % request.headers.get('content-length'))
    # print body content
    body_bytes = request.get_data()
    # replace image raw data with string '<image raw data>'
    body_sub_image_data = re.sub(b'(\r\n\r\n)(.*?)(\r\n--)', br'\1<image raw data>\3', body_bytes, flags=re.DOTALL)
    print(body_sub_image_data.decode('utf-8'))


@app.route('/facerec', methods=['POST', 'GET'])
def face_recognition():
    if request.method == 'POST':
        # Print request url, headers and content
        print_request(request)

        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files.get('file')
        # if user does not select file, browser also submit an empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)

        if allowed_file(file.filename):
            result = face_rec(file)
            # filename = secure_filename(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # resp_data = {
            #     'results': result
            # }
            resp_data = result
            timestamp = datetime.now().strftime("%Y-%d-%mT%H:%M:%SZ")

            # get parameters from url if any.
            # facial_features parameter:
            param_features = request.args.get('facial_features', '')
            if param_features.lower() == 'true':
                facial_features = find_facial_features(file)
                # append facial_features to resp_data
                resp_data.update({'facial_features': facial_features})

            # face_locations parameter:
            param_locations = request.args.get('face_locations', '')
            if param_locations.lower() == 'true':
                face_locations = find_face_locations(file)
                resp_data.update({'face_locations': face_locations})

            return jsonify({
                "predict": {
                    "data": resp_data,
                    "status": {
                        "code": 200,
                        "sucess": True,
                        "timestamp": timestamp,
                    },
                }
            })

    return render_template('facerec/index.html')


@app.route('/')
def hello_world():
    return jsonify({'message': 'Hello, World!'})


# Run
# When debug = True
app.run(host='0.0.0.0', port='5000')
