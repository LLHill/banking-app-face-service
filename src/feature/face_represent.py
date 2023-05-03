from deepface.commons import functions
from deepface import DeepFace
import cv2
import numpy as np
import base64
import pickle
import traceback

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
        face = pickle.loads(row[0])[0, :, :, :][:, :, ::-1]
        face *= 255
        img_pair.append([base_img, face])
    verified_dict = DeepFace.verify(img1_path = img_pair, model_name='Dlib', enforce_detection = False, detector_backend = 'ssd', prog_bar = False)
    verified = 0
    for key in verified_dict:
        if verified_dict[key]['verified']:
            verified += 1
    print(f'num of true face: {verified}')
    if (verified > 4):
        if (analysis == True):
            return True
        else:
            return analysis
    return False


def analyze_face(base_img, emotion):
    analysis_dict = DeepFace.analyze(img_path = base_img, actions = ['emotion'], detector_backend = 'ssd', prog_bar = False)
    dominant_emotion = analysis_dict['dominant_emotion']
    if (dominant_emotion == emotion):
        return True
    return f'get {dominant_emotion} instead of {emotion}'

def process_face(userId, base_img, face_num):
    if userId == None or base_img == None:
        return 'None'
    try:
        result = detect_face(base_img)
        if face_num == 0:
            is_existed, detected_user = check_existed_face(base_img)
            print(f'detected user: {detected_user} and user: {userId}')
            if is_existed and detected_user != userId:
                store_db.delete_user(userId)
                return 'Existed'
        store_db.store_data(userId, result[4].dumps())
        result.pop()
        return result
    except Exception as e:
        traceback.print_exc()
        return 'None'


def detect_face(base_img):
    # test = DeepFace.represent(base_img, detector_backend = 'ssd', enforce_detection = False)
    face_img, region = functions.preprocess_face(base_img, detector_backend = 'ssd',return_region = True)
    x, y, w, h = region
    max_h,max_w, _ = decode_b64(base_img).shape
    x, y, w, h = x/max_w, y/max_h, w/max_w, h/max_h
    return [x, y, w, h, face_img]

def check_existed_face(base_img):
    faces_arr = []
    user_list = []
    img_pair = []
    all_faces = store_db.get_top6_each_user()
    if not all_faces:
        return False, 'None'
    user_list.append(all_faces[0][1])
    for row in all_faces:
        if row[1] != user_list[-1]:
            faces_arr.append(img_pair)
            user_list.append(row[1])
            img_pair = []
        face = pickle.loads(row[0])[0, :, :, :][:, :, ::-1]
        face *= 255
        img_pair.append([base_img, face])
    faces_arr.append(img_pair)
    for idx in range(len(faces_arr)):
        verified = 0
        verified_dict = DeepFace.verify(img1_path = faces_arr[idx], model_name='Dlib', enforce_detection = False, detector_backend = 'ssd', prog_bar = False)
        for key in verified_dict:
            if verified_dict[key]['verified']:
                verified += 1
        print(f'num of true face: {verified} for user: {user_list[idx]}')
        if (verified > 5):
            return True, user_list[idx]

    return False, 'User face is not existed in the database'

    
def recognize_face(base_img):
    if base_img == None:
        return 'None'
    try:
        functions.preprocess_face(base_img, detector_backend = 'ssd',return_region = True)
        is_existed, user_id = check_existed_face(base_img)
        return user_id
    except:
        return 'None'

def decode_b64(base_img):
    encoded_data = base_img.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

