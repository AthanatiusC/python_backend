#
# client.py
# Vision-Intelligent-Platform
#
# Created by Purwo Widodo on 29/01/2020.
# Copyright © 2019 Purwo Widodo. All rights reserved.
#

import requests
import json
import sys

# def test_facematch():
#     url = 'http://127.0.0.1:5001/facematch'
#     files = {
#         'file1': open('datasets/azhar.jpeg', 'rb'), 'file2': open('datasets/purwo.jpeg', 'rb')
#     }
#     resp = requests.post(url, files=files)
#     print('facematch response:\n', json.dumps(resp.json()))


def test_facerec():
    url = 'http://127.0.0.1:5000/facerec'
    files = {
        'file': open('C:\xampp\htdocts\endpointfr\img_face/Azhar/10374_azhar.jpeg', 'rb')
        #'file': open('/var/www/html/Backend/facerec_by_images/datasets/'+sys.argv[1], 'rb')
    }
    resp = requests.post(url, files=files)
    data = resp.json()
    print(data["predict"]["data"]["name"])
    print('facerec response:\n', json.dumps(resp.json()))


def main():
    # test_facematch()
    test_facerec()


if __name__ == '__main__':
    main()
