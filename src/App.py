from flask import Flask, request
from flask_socketio import SocketIO, emit
from feature import face_process
import time

app = Flask(__name__) 
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def init_connect():
    print('connected')

@socketio.on('detect')
def detect(payload):
    userId = payload['userId']
    img = payload['img']
    face_num = payload['num']
    face_area = face_process.register_face(userId, img, face_num)
    emit("detected",{'payload': face_area})

@socketio.on('recognize')
def recognize(payload):
    # print('recognizing face')
    img = payload['img']
    user_id = face_process.login_face(img)
    emit("recognized",{'payload': user_id})

@socketio.on('verify')
def verify(payload):
    userId = payload['userId']
    img = payload['img']
    emotion = payload['emotion']
    isVerified = face_process.analyze_face(userId, img, emotion)
    emit('verified', {'payload': isVerified})

@socketio.on('disconnect')
def on_disconnect():
    print('disconnect')



if __name__=="__main__":
    socketio.run(app)