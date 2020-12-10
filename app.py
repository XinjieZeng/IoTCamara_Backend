from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import configs
from facedetect import detect_face
from facecompare import compare_face
from open_garage_door import open_garage_door
from state import SUCCESS
from state import FAIL


app = Flask(__name__)
app.config.from_object(configs)
db = SQLAlchemy(app)


class Photo(db.Model):
    __tablename__ = 'photo'
    photo_id = db.Column(db.INTEGER, primary_key=True)
    address = db.Column(db.String(50))
    user_id = db.Column(db.Integer)
    face_token = db.Column(db.String(50))


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.INTEGER, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))


@app.route('/login', methods= ['POST'])
def index():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter(User.username == username, User.password == password).first()

    if not user:
        return FAIL

    return SUCCESS


@app.route('/opengarage', methods=['POST'])
def open_garage():
    # get the multipart file
    file = request.files["file"].read()

    # detect faces
    try:
        face_token_1 = detect_face(file)
    except ValueError:
        return SUCCESS

    face_token_2 = Photo.query.filter(Photo.user_id == 1).first().face_token

    # call 3PP to compare faces
    if compare_face(face_token_1, face_token_2) == SUCCESS:
        return open_garage_door()
    return FAIL


@app.route('/addphoto', methods=['POST'])
def add_photo():
    # get the multipart file
    file = request.files["file"].read()
    filename = request.form.get("filename")

    # call 3PP to get face token
    try:
        face_token = detect_face(file)
    except ValueError:
        return FAIL

    # save the image and face token in database
    save_photo_in_database(filename, face_token)
    return SUCCESS


def save_photo_in_database(filename, token):
    photo = Photo(address=filename, user_id=1, face_token=token)
    db.session.add(photo)
    db.session.commit()


if __name__ == '__main__':
    app.run(debug=True, host="192.168.254.73")









