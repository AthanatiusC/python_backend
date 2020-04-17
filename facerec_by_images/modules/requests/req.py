import requests
import json
import time
# from modules.crop.recognize import FaceRecog

# GET : List result crop
# id_cam = FaceRecog(camID)
url_list_crop = "http://127.0.0.1:8001/api/listResultCrop?id_cam=1"

payload = {}
headers= {}

r_list_crop = requests.request("GET", url_list_crop, headers=headers, data = payload)
faces = json.loads(r_list_crop.text.encode('utf8'))
# print(faces[2]['picture'])
for face in faces:
    # time.sleep(0.5)
    # print(face['picture'])
    url_facerec = "http://127.0.0.1:5000/facerec"
    files = {
        'file': open("/var/www/html/Backend/facerec_by_images/datasets/crop"+face['picture'], 'rb')
    }
    resp = requests.post(url_facerec, files=files)
    # print('Response:\n', json.dumps(resp.json()))
    output = json.dumps(resp.json())

    print(output)