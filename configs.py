from datetime import timedelta

HOSTNAME = 'mysql'
PORT=3306
DATABASE = 'IoTCamera'
USERNAME = 'root'
PASSWORD = '123456'
DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?auth_plugin=mysql_native_password'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI=DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS=True
PHOTO_BASE_PATH = r'/Users/xinjiezeng/PycharmProjects/flaskProject/images/'
DETECT_FACE_URL = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
COMPARE_FACE_URL = 'https://api-cn.faceplusplus.com/facepp/v3/compare'
GARAGE_CREDENTIAL_URL = 'https://api.myqdevice.com/api/v5/Login'
KEY = "vTLWlxe8ooTcPutTopW624ANrOthhNeh"
SECRET = "XXXXXXXXXXX"
MY_Q_USERNAME = 'xxxxxx'
MY_Q_PASSWORD = 'xxxxxxx'
SECRET_KEY='abcdefg'
PERMANENT_SESSION_LIFETIME = timedelta(days=7)
