#
# camera.py
# facerec_by_images
#
# Created by Purwo Widodo on 03/02/2020.
# Copyright © 2019 Purwo Widodo. All rights reserved.
#

import cv2


class VideoCamera(object):
    def __init__(self, ip_addr, username, password, cam_path, id_cam):
        # if username == "-":
        #     self.data = 10
        # elif username != "-":
        #     self.data = 'rtsp://'+username+':'+password+'@'+ip_addr+''+cam_path+''
        # self.video = cv2.VideoCapture(self.data)
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        # Grab a single _frame of video
        ret, _frame = self.video.read()
        return _frame


if __name__ == '__main__':
    cam = VideoCamera(ip_addr="", username="", password="", cam_path="")
    while True:
        frame = cam.get_frame()

        # show the framexs
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    # do a bit of cleanup
    cv2.destroyAllWindows()
    print('finish')
