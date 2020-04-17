import face_recognition as fr
from threading import Thread
from modules.gender_age import dex
import requests
import json
import time
# setup model
dex.eval()


def compare_faces(file1, file2):
    """
    Compare two images and return True / False for matching.
    """
    # Load the jpg files into numpy arrays
    image1 = fr.load_image_file(file1)
    image2 = fr.load_image_file(file2)

    # Get the face encodings for each face in each image file
    # Assume there is only 1 face in each image, so get 1st face of an image.
    image1_encoding = fr.face_encodings(image1)[0]
    image2_encoding = fr.face_encodings(image2)[0]

    # results is an array of True/False telling if the unknown face matched anyone in the known_faces array
    results = fr.compare_faces([image1_encoding], image2_encoding, tolerance=0.5)
    return results[0]


# Each face is tuple of (Name,sample image)
# known_faces = [
#         ('Purwo', 'C:/xampp/htdocts/endpointfr/img_face/purwo/8213_purwo.jpeg'), 
#         ('Azhar', 'C:/xampp/htdocts/endpointfr/img_face/Azhar/10374_azhar.jpeg'), 
#         ('Sultan', 'C:/xampp/htdocts/endpointfr/img_face/Sultan/7419_sultan.jpeg'), 
#         ('Lex', 'C:/xampp/htdocts/endpointfr/img_face/Lex/11560_laxlex.jpg'), 
#         ('Lex', 'C:/xampp/htdocts/endpointfr/img_face/Lex/9934_lex.jpeg'), 
#         ('Leonaldy', 'C:/xampp/htdocts/endpointfr/img_face/Leonaldy/10912_leonaldy2.jpeg'), 
#         ('Handika', 'C:/xampp/htdocts/endpointfr/img_face/Handika/9621_dika.jpeg'), 
#         ('Raffi', 'C:/xampp/htdocts/endpointfr/img_face/Raffi/6873_raffi.jpeg'),
#         ('Sultan', 'C:/xampp/htdocts/endpointfr/img_face/Sultan/7419_sultan.jpeg'), 
#         ('Lex', 'C:/xampp/htdocts/endpointfr/img_face/Lex/11560_laxlex.jpg'), 
#         ('Lex', 'C:/xampp/htdocts/endpointfr/img_face/Lex/9934_lex.jpeg'), 
#         ('Leonaldy', 'C:/xampp/htdocts/endpointfr/img_face/Leonaldy/10912_leonaldy2.jpeg')
# ]

known_faces = []
def get_face():
    while True:
        time.sleep(3)
        data = requests.get("http://127.0.0.1:8001/api/listFace")
        json = data.json()
        
        for face in json:
            directory = "C:/xampp/htdocts/endpointfr/public/"+face["dirname"]+"/"+face["picture"]
            # print("Preparring : {}".format(directory))
            known_faces.append((face["name"], directory))

        #  print(list_face)
t1 = Thread(target = get_face)
t1.setDaemon(True)
t1.start()

unknown_faces = [
    'trash/azhar.jpg'
]

def cekVariable():
    while True:
        time.sleep(3)
        #print(known_faces)
t2 = Thread(target = cekVariable)
t2.setDaemon(True)
t2.start()

def face_rec(file):
    """
    Return name for a known face, otherwise return 'Uknown'.
    """
    for name, known_file in known_faces:
        try:
            if compare_faces(known_file, file):
                age, female, male = dex.estimate(known_file)
                # gender = "woman: {:.3f}, man: {:.3f}".format(female, male)
                _age = "{:.0f}".format(age)
                if "{:.3f}".format(female) > "{:.3f}".format(male):
                    gender = "Female"
                else:
                    gender = "Male"
                return {
                    "name": name,
                    # "gender": gender,
                    # "age": _age,
                }
        except :
            return 'Unknown'


def find_facial_features(file):
    # Load the jpg file into a numpy array
    image = fr.load_image_file(file)

    # Find all facial features in all the faces in the image
    face_landmarks_list = fr.face_landmarks(image)

    # return facial features if there is only 1 face in the image
    if len(face_landmarks_list) != 1:
        return {}
    else:
        return face_landmarks_list[0]


def find_face_locations(file):
    # Load the jpg file into a numpy array
    image = fr.load_image_file(file)

    # Find all face locations for the faces in the image
    face_locations = fr.face_locations(image)

    # return facial features if there is only 1 face in the image
    if len(face_locations) != 1:
        return []
    else:
        return face_locations[0]
