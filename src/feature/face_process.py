from deepface.commons import functions
from deepface import DeepFace
import cv2
import numpy as np
import pickle
import traceback
from deepface.commons import functions, distance as dst

from feature import store_db

MODEL_NAME = 'Facenet512'
NORMALIZATION = 'Facenet'
METRIC = 'cosine'
DETECTOR = 'dlib'


def analyze_face(userId, base_img, emotion):
    try:
        face, _ = detect_face(base_img)
        embedding_face = represent_face(face)
    except Exception as e:
        traceback.print_exc()
        return 'None'
    verified = 0
    threshold = dst.findThreshold(MODEL_NAME, METRIC)
    odbc_faces = store_db.get_data(userId)
    for row in odbc_faces:
        face_str = row[0]
        db_face = list(map(float, face_str.split(" ")))
        distance = compute_distance(embedding_face, db_face)
        if distance <= threshold:
            verified += 1
    if verified < 5:
        return False
    emotion_analysis = DeepFace.analyze(img_path = base_img, 
                                        actions = ('emotion'), 
                                        detector_backend = 'ssd', 
                                        silent=True)
    detected_emotion = emotion_analysis[0]['dominant_emotion']
    if detected_emotion == emotion:
        return True
    return f'get {detected_emotion} instead of {emotion}'


def register_face(userId, base_img, face_num):
    if userId == None or base_img == None:
        return 'None'
    try:
        face, face_regions = detect_face(base_img)
        embedding_face = represent_face(face)
        print(face_num)
        if face_num == 0:
            is_existed, recognized_id = recognize_face(embedding_face, 4)
            if is_existed and recognized_id != userId:
                print(f'faces of user {userId} are already registered with {recognized_id}')
                store_db.delete_user(userId)
                return 'Existed'
        embedding_str = ' '.join(str(x) for x in embedding_face)
        store_db.store_data(userId, embedding_str)
        return face_regions
    except Exception as e:
        return 'None'


def login_face(base_img):
    if base_img == None:
        return 'None'
    try:
        face, _ = detect_face(base_img)
        embedding_face = represent_face(face)
        _, recognized_id = recognize_face(embedding_face, 5)
        return recognized_id
    except Exception as e:
        return 'None' 


def detect_face(base_img):
    if base_img == None:
        raise Exception('No input face')
    try:
        target_size = functions.find_target_size(model_name=MODEL_NAME)
        face = functions.extract_faces(img= base_img, target_size = target_size, detector_backend = DETECTOR)
        return face[0][0], [face[0][1]['x'], face[0][1]['y'], face[0][1]['w'], face[0][1]['h']]
    except Exception as e:
        raise Exception(e)


def represent_face(face_img):
    try:
        embedding_obj = DeepFace.represent(img_path = face_img
                    , model_name = MODEL_NAME
                    , enforce_detection = False
                    , detector_backend = "skip"
                    , align = True
                    , normalization = NORMALIZATION
                    )
        return embedding_obj[0]["embedding"]
    except Exception as e:
        raise Exception(e)


def recognize_face(embedding_face, min_face):
    user_list = []
    threshold = dst.findThreshold(MODEL_NAME, METRIC)
    try:
        all_faces = store_db.get_top6_each_user()
        if not all_faces:
            return False, 'None'
        for row in all_faces:
            face_str = row[0]
            db_face = list(map(float, face_str.split(" ")))
            distance = compute_distance(embedding_face, db_face)
            if distance <= threshold:
                user_list.append(row[1])
        print(user_list)
        if not user_list:
            return False, 'None'
        users, counts = np.unique(np.array(user_list), return_counts=True)
        if np.max(counts) > min_face:
            return True, int(users[np.argmax(counts)])
        return False, 'None'
    except Exception as e:
        raise Exception(e)


def compute_distance(representation_1, representation_2):
    if METRIC == 'cosine':
        return dst.findCosineDistance(representation_1, representation_2)
    elif METRIC == 'euclidean':
        return dst.findEuclideanDistance(representation_1, representation_2)
    elif METRIC == 'euclidean_l2':
        return dst.findEuclideanDistance(dst.l2_normalize(representation_1), dst.l2_normalize(representation_2))
    else:
        raise ValueError("Invalid distance_metric passed - ", METRIC)
