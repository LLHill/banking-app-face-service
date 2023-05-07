# Face Service
Python server for face recognition tasks

## How to use
1.  Install python 3
2.  Clone the source code
3.  Then install requirements with  `pip install -r requirements.txt`
4.  Set up the database information (SERVER, DATABASE, USERNAME, PASSWORD) in `src\feature\store_db.py` file
5.  Set up the Deepface model information in `src\feature\face_process.py` (https://github.com/serengil/deepface)
4.  Run the server with `python src\App.py`