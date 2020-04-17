import cv2
import os
import time
import sys
import random
import requests
import datetime

username = sys.argv[1]
password = sys.argv[2]
ipaddr = sys.argv[3]
path = sys.argv[4]
idcam = sys.argv[5]

urlApi = "http://teslar.test"
fullpath = "/Users/nugrahas/Sites/"
def capture(video, path_output_dir):
    vidcap = cv2.VideoCapture(video)
    count = 0
    if vidcap.isOpened():
        success, image = vidcap.read()
        if success:

            acak = random.randint(10000, 50000)
            gambar = 'thumbnail-'+str(acak)+'.png'
            data = {
                    'thumbnail': gambar,
                }
            print(data)
            save_thumbnail(idcam, data)
            #gambar yang tersimpan akan di beri nama gambar.png dan ukurannya menjadi h 600 px dan w 400px
            cv2.imwrite(os.path.join(path_output_dir, gambar), cv2.resize(image,(600,400)))
            print("capture ok")
        else :
            print("Gagal Load Kamera")
    vidcap.release()


def save_thumbnail(id, path):
    while True:
        try:
            api = "/api/camera/thumbnail/" + id
            response = requests.post(url=urlApi + api, data=path)
            return response
        except:
            pass
        time.sleep(1)

# def logger(msg, prn=True):
#     if prn:
#         print(msg)

#     joinusername = '_'.join(list(username))
#     logfile = open("/tmp/log-tes.txt", "a")
#     logfile.write(
#         "[" + datetime.datetime.now().strftime("%y-%m-%d %H:%M") + "] " + msg + "\n")
#     logfile.close()

#gambar akan di akses dari rtsp kamera dan di simpan dalam folder di dalam server

# capture('rtsp://admin:admin12345@192.168.1.16:554/Streaming/channels/101', 'public/images/')
capture('rtsp://'+username+':'+password+'@'+ipaddr+':554'+path+'', fullpath+'endpointfr/public/images/')

time.sleep (2)