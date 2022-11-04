import pyodbc


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
    



if __name__ != "__main__":
    sql_db = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+SERVER+
    ';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD)
    cursor = sql_db.cursor()



