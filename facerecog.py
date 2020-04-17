#
# facerecog.py
# Vision-Intelligent-Platform
#
# Created by Purwo Widodo on 09/01/2020.
# Copyright © 2019 Purwo Widodo. All rights reserved.
#

import os

import cv2
import face_recognition
import numpy as np
import camera


class Recognition:
    def __init__(self,cam_type,ip_add,username,password,id_camRTSP):
        self.camera = camera.StreamCamera(cam_type,ip_add,username,password,id_camRTSP)

        self.known_face_encodings = []
        self.known_face_names = []

        dirname = "knowns"
        files = os.listdir(dirname)
        for filename in files:
            name, ext = os.path.splitext(filename)
            if ext == '.jpg':
                self.known_face_names.append(name)
                pathname = os.path.join(dirname, filename)
                img = face_recognition.load_image_file(pathname)
                face_encoding = face_recognition.face_encodings(img)[0]
                self.known_face_encodings.append(face_encoding)

        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process = True

    def __del__(self):
        del self.camera

    def get_frame(self):
        frames = self.camera.get_frame()
        small_frame = cv2.resize(frames, (0, 0), fx=0.25, fy=0.25)
        rgb_frame = small_frame[:, :, ::-1]

        if self.process:
            self.face_locations = face_recognition.face_locations(rgb_frame)
            self.face_encodings = face_recognition.face_encodings(rgb_frame, self.face_locations)

            self.face_names = []

            for face_encoding in self.face_encodings:
                distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                min_value = min(distances)

                name = 'unknown'
                if min_value < 0.6:
                    index = np.argmin(distances)
                    index = int(index)
                    name = self.known_face_names[index]

                self.face_names.append(name)

        self.process = not self.process

        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frames, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frames, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            #img = cv2.imread(frames, 1)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frames, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        return frames

    def jpg_bytes(self):
        frames = self.get_frame()
        ret, jpg = cv2.imencode('.jpg', frames)
        return jpg.tobytes()


if __name__ == '__main__':
    recognition = Recognition()
    print(recognition.known_face_names)
    while True:
        frame = recognition.get_frame()

        cv2.imshow('frame', frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

    cv2.destroyAllWindows()
