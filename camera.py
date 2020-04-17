#
# camera.py
# Vision-Intelligent-Platform
#
# Created by Purwo Widodo on 09/01/2020.
# Copyright © 2019 Purwo Widodo. All rights reserved.
#

import cv2


class StreamCamera(object):
    def __init__(self,cam_type,ip_add,username,password,id_camRTSP):
        #if cam_type == 'rtsp':
        #if username != '-':
        #    self.video = cv2.VideoCapture('rtsp://'+username+':'+password+'@'+ip_add+'/Streaming/channels/'+id_camRTSP+'')
        #else:
        #   self.video = cv2.VideoCapture(cam_type)
        if username == '-':
            data = 0
        elif username != '-':
            data = 'rtsp://'+username+':'+password+'@'+ip_add+'/Streaming/channels/'+id_camRTSP+''
        self.video = cv2.VideoCapture(data)
    def __delete__(self):
        self.video.release()

    def get_frame(self):
        ret, frames = self.video.read()
        return frames


if __name__ == '__main__':
    cam = StreamCamera()
    while True:
        frame = cam.get_frame()

        cv2.imshow('Frame', frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

    cv2.destroyAllWindows()
