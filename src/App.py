from flask import Flask, request
from flask_socketio import SocketIO, emit
from feature import face_represent
import time

app = Flask(__name__) 
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def init_connect():
    print('connected')

@socketio.on('detect')
def detect(payload):
    # print('receive messsage')
    userId = payload['userId']
    img = payload['img']
    face_area = face_represent.detect_face(userId, img)
    emit("detected",{'payload': face_area})

@socketio.on('verify')
def verify(payload):
    userId = payload['userId']
    img = payload['img']
    emotion = payload['emotion']
    isVerified = face_represent.verify_face(userId, img, emotion)
    emit('verified', {'payload': isVerified})

@socketio.on('disconnect')
def on_disconnect():
    print('disconnect')



if __name__=="__main__":
    socketio.run(app)


    

