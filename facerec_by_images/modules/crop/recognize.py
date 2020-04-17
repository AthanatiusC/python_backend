#
# recognize.py
# facerec_by_images
#
# Created by Purwo Widodo on 03/02/2020.
# Copyright © 2019 Purwo Widodo. All rights reserved.
#

import face_recognition
import cv2
import os
import numpy as np
import sys, requests
import string
from modules.crop import camera
import random
import time
import json
from threading import Thread
from queue import Queue
# from __future__ import generator_stop

# from modules.base.util import list_faces


class FaceRecog:

    def __init__(self, ip_addr, username, password, cam_path, id_cam):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.camID = id_cam
        self.camera = camera.VideoCamera(ip_addr, username, password, cam_path, id_cam)

        self.known_face_encodings = []
        self.known_face_names = []
        self.not_stopped = True
        self.api_container = Queue(maxsize=20)


        # Load sample pictures and learn how to recognize it.
        dirname = "C:/xampp/htdocs/endpointfr/public/img_face"
        folders = os.listdir(dirname)
        for foldername in folders:
            self.known_face_names.append(foldername)
            full_path =dirname+"/"+foldername
            files = os.listdir(full_path)
            for filename in files:
                print(full_path)
                print(full_path+"/"+filename)
                img = face_recognition.load_image_file(os.path.join(full_path+"/"+filename))
                try:
                    face_encoding = face_recognition.face_encodings(img)[0]
                except:
                    continue
                self.known_face_encodings.append(face_encoding)
                    
        # Initialize some variables
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True
        self.counter = 0
        self.thread = Thread(target=self.send_api)
        self.thread.daemon = True
        self.thread.start()

    def __del__(self):
        self.thread.join()
        del self.camera

    def send_api(self):
        while self.not_stopped:
            if self.api_container.not_empty:
                url_store_crop_face = "http://127.0.0.1:8001/api/storeCropFace"
                r_store_crop_face = requests.get(url=url_store_crop_face, params=self.api_container.get())
                try:
                    print(r_store_crop_face.json())
                except:
                    pass
    
    def get_frame(self):
        c_path = os.getcwd()
        # Grab a single frames of video
        frames = self.camera.get_frame()

        # Resize frames of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frames, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frames of video to save time
        # if self.process_this_frame:
            # Find all the faces and face encodings in the current frames of video
        self.face_locations = face_recognition.face_locations(rgb_small_frame)
        self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

        self.face_names = []
        for face_encoding in self.face_encodings:
            # See if the face is a match for the known face(s)
            start_time = time.time()
            match = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            min_value = min(match)
            name = ""
            if min_value < 0.5:
                index_name = np.argmin(match)
                name = self.known_face_names[index_name:]
                self.face_names.append(name[0])
            else:   
                name = "Unknown"
                self.face_names.append(name)
            print("recognize took {} sec".format(time.time()-start_time))

        # self.process_this_frame = not self.process_this_frame

        # Display the results
        # list_faces() 

        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            # Scale back up face locations since the frames we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frames, (left, top), (right, bottom), (0, 0, 255), 2)
            crop = frames[top:bottom, left:right]
            nameFile = ''.join(random.sample((string.ascii_uppercase+string.digits),12))
            # cv2.imwrite(c_path + "/datasets/crop/cropped/" + nameFile + ".jpeg", crop)
            if name != "":
                if self.api_container.not_full:
                    param_store_crop_face = {'nameFile': nameFile+'.jpeg', 'id_cam': self.camID, 'name': name, 'status_people': 1}
                    self.api_container.put(param_store_crop_face) 
            


            # url = 'http://127.0.0.1:5000/facerec'
            # files = {
            #     'file': open(c_path + "/datasets/crop/cropped/" + nameFile+".jpeg", 'rb')
            # }
            # resp = requests.post(url, files=files)
            # data = resp.json()

            # url_store_crop_face = "http://127.0.0.1:8001/api/storeCropFace"
            # param_store_crop_face = {'nameFile': nameFile+'.jpeg', 'id_cam': self.camID, 'name': name, 'status_people': 0}
            # r_store_crop_face = requests.get(url=url_store_crop_face, params=param_store_crop_face)
            # cv2.rectangle(frames, (left, bottom), (right, bottom), (0, 0, 255), 1)


            # # GET : List result crop
            # url_list_crop = "http://127.0.0.1:8001/api/listResultCrop?id_cam=1&limit=5"+str(self.camID)

            # payload = {}
            # headers= {}

            # r_list_crop = requests.request("GET", url_list_crop, headers=headers, data = payload)
            # faces = json.loads(r_list_crop.text.encode('utf8'))
            # for face in faces:
            #     print(face['picture'])
            #     url_facerec = "http://127.0.0.1:5000/facerec"
            #     files = {
            #         'file': open("/var/www/html/Backend/facerec_by_images/datasets/crop"+face['picture'], 'rb')
            #     }
            #     resp = requests.post(url_facerec, files=files)
            #     print('Response:\n', json.dumps(resp.json()))
            #     output = json.dumps(resp.json())
            # Draw a label with a name below the face
            # cv2.rectangle(frames, (left, bottom - 35), (right, bottom), (0, 0, 255), 1)
            # list_faces()

        return frames

    def get_jpg_bytes(self):
        _frame = self.get_frame()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        try:
            ret, jpg = cv2.imencode('.jpg', _frame)
        except:
            return
        return jpg.tobytes()


# if __name__ == '__main__':
#     face_recog = FaceRecog(ip_addr="", username="", password="", cam_path="", id_cam="")
#     print(face_recog.known_face_names)
#     while True:
#         frame = face_recog.get_frame(id_cam)

#         # show the frame
#         cv2.imshow("Frame", frame)
#         key = cv2.waitKey(1) & 0xFF

#         # if the `q` key was pressed, break from the loop
#         if key == ord("q"):
#             break

#     # do a bit of cleanup
#     cv2.destroyAllWindows()
#     print('finish')
