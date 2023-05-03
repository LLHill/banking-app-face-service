import pyodbc
import pickle
from deepface import DeepFace
import cv2
import numpy as np


SERVER = 'localhost,1433'
DATABASE = 'bankapp'
USERNAME = 'sa'
PASSWORD = 'Hieu2301*'


def store_data(userId, img):
    print(f'storing data: {userId}')
    cursor.execute('''
    INSERT INTO dbo.face (user_id, face_img) VALUES (?,?);
    ''',
    userId, img)
    sql_db.commit()
    print('store face data successfully')

def get_data(userId):
    print(f'getting data: {userId}')
    cursor.execute('''
    SELECT face_img FROM dbo.face WHERE user_id = ?
    ''',
    userId)
    return cursor.fetchall()
    
def get_top6_each_user():
    cursor.execute('''
    SELECT face_img, user_id, rn
    FROM 
    ( SELECT face_img, user_id, id, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY id DESC) AS rn FROM dbo.face) tmp 
    WHERE rn <= 6
    ORDER BY user_id
    ''')
    return cursor.fetchall()

def delete_user(userId):
    print(f'deleting user with id: {userId}')
    cursor.execute('''
    DELETE FROM dbo.app_user WHERE id = ?
    ''',
    userId)
    sql_db.commit()
    print('delete user successfully')


if __name__ != "__main__":
    sql_db = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+SERVER+
    ';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD)
    cursor = sql_db.cursor()
    # num_img = 0
    # all_faces = get_data(4)
    # for row in all_faces:
    #     face = pickle.loads(row[0])[0, :, :, :][:, :, ::-1]
    #     face *= 255
    #     cv2.imwrite(f"face_{num_img}.jpg", face)
    #     num_img +=1

    # print(face_arr)
    # print('--------------')
    # print(user_list)
    # all_faces = get_top3_each_user()
    # for row in all_faces:
    #     face = pickle.loads(row[0])[0, :, :, :]
    #     test = DeepFace.represent(face, enforce_detection = False)
    # print('done')