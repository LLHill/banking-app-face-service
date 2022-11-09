import pyodbc
import pickle
from deepface import DeepFace


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
    
def get_top3_each_user():
    cursor.execute('''
    SELECT face_img, user_id, rn
    FROM 
    ( SELECT face_img, user_id, id, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY id DESC) AS rn FROM dbo.face) tmp 
    WHERE rn <= 3
    ORDER BY user_id
    ''')
    return cursor.fetchall()

def delete_user(userId):
    print(f'deleting user with id: {userId}')
    cursor.execute('''
    DELETE FROM dbo.[user] WHERE id = ?
    ''',
    userId)
    sql_db.commit()
    print('delete user successfully')


if __name__ != "__main__":
    sql_db = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+SERVER+
    ';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD)
    cursor = sql_db.cursor()
    # face_arr = []
    # user_list = []
    # img_pair = []
    # all_faces = get_top3_each_user()
    # user_list.append(all_faces[0][1])
    # for row in all_faces:
    #     if row[1] != user_list[-1]:
    #         face_arr.append(img_pair)
    #         user_list.append(row[1])
    #         img_pair = []
    #     img_pair.append('face')

    # print(face_arr)
    # print('--------------')
    # print(user_list)
    # all_faces = get_top3_each_user()
    # for row in all_faces:
    #     face = pickle.loads(row[0])[0, :, :, :]
    #     test = DeepFace.represent(face, enforce_detection = False)
    # print('done')



