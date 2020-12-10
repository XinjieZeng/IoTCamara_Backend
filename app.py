from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import configs
from facedetect import detect_face
from facecompare import compare_face

app = Flask(__name__)
PHOTO_BASE_PATH = r'/Users/xinjiezeng/PycharmProjects/flaskProject/images/'

app.config.from_object(configs)
db = SQLAlchemy(app)


class Photo(db.Model):
    __tablename__ = 'photo'
    photo_id = db.Column(db.INTEGER, primary_key=True)
    address = db.Column(db.String(50))
    user_id = db.Column(db.Integer)
    face_token = db.Column(db.String(50))


@app.route('/opengarage', methods=['POST'])
def open_garage():
    # get the multipart file
    file = request.files["file"].read()

    # detect faces
    try:
        face_token_1 = detect_face(file)
    except ValueError:
        return "fail"

    face_token_2 = Photo.query.filter(Photo.user_id == 1).first().face_token

    # call 3PP to compare faces
    return compare_face(face_token_1, face_token_2)


def open_garage():
    return True


@app.route('/addphoto', methods=['POST'])
def add_photo():
    # get the multipart file
    file = request.files["file"].read()
    filename = request.form.get("filename")

    # call 3PP to get face token
    try:
        face_token = detect_face(file)
    except ValueError:
        return "fail"

    # save the image and face token in database
    save_photo_in_database(filename, face_token)
    return "success"


def save_photo_in_database(filename, token):
    photo = Photo(address=filename, user_id=1, face_token=token)
    db.session.add(photo)
    db.session.commit()


if __name__ == '__main__':
    app.run(debug=True, host="192.168.254.73")








# @app.route('/login', methods= ['POST'])
# def index():
#     print(request.is_json)
#     content = request.get_json()
#     print(content)
#
#     username = content['username']
#     password = content['password']
#
#     cursor = mysql.connection.cursor()
#     user_name = (username,)
#     user_id = cursor.execute("""SELECT user_id from users where username = %s""", user_name)
#     user = cursor.fetchall()
#
#     if not user:
#         cursor.close()
#         return "invalid"
#
#     cursor.execute("""SELECT password from credentials where user_id = %s and password = %s""", (user_id, password,))
#     data = cursor.fetchall()
#     cursor.close()
#
#     if not data:
#         return "invalid"
#
#     return "successful"
