from deepface.commons import functions
from deepface import DeepFace
import cv2
import numpy as np
import base64
import pickle
from PIL import Image

from feature import store_db

def verify_face(userId, base_img, emotion):
    try:
        analysis = analyze_face(base_img, emotion)
    except Exception as e:
        print(e)
        return 'None'
    img_pair = []
    odbc_faces = store_db.get_data(userId)
    for row in odbc_faces:
        face = pickle.loads(row[0])[0, :, :, :]
        # test = DeepFace.represent(face, detector_backend = 'ssd', enforce_detection = False)
        img_pair.append([base_img, face])
    verified_dict = DeepFace.verify(img1_path = img_pair, enforce_detection = False, detector_backend = 'ssd', prog_bar = False)
    verified = 0
    for key in verified_dict:
        verified += 1 if verified_dict[key]['verified'] else verified
    print(verified)
    if (verified/len(verified_dict) > 0.6):
        if (analysis == True):
            return True
        else:
            return analysis
    return False


def analyze_face(base_img, emotion):
    analysis_dict = DeepFace.analyze(img_path = base_img, actions = ['emotion'], detector_backend = 'ssd', prog_bar = False)
    print(analysis_dict)
    dominant_emotion = analysis_dict['dominant_emotion']
    if (dominant_emotion == emotion):
        return True
    return f'get {dominant_emotion} instead of {emotion}'


def detect_face(userId, base_img):
    try:
        if base_img == None:
            raise Exception('The input img is null')
        if userId == None:
            raise Exception('The input user is null')
        # test = DeepFace.represent(base_img, detector_backend = 'ssd', enforce_detection = False)
        face_img, region = functions.preprocess_face(base_img, detector_backend = 'ssd',return_region = True)
        x, y, w, h = region
        max_h,max_w, _ = decode_b64(base_img).shape
        x, y, w, h = x/max_w, y/max_h, w/max_w, h/max_h
        store_db.store_data(userId, face_img.dumps())
        # print(x, y, w, h)
        # print('-----', max_w, max_h)
        return [x, y, w, h]
    except Exception as e:
        print(f'Error occurs: {e}')
        return 'None'


def decode_b64(base_img):
    encoded_data = base_img.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

