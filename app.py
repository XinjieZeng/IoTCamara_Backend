from flask import Flask, request
from facecompare import compare_face
import io
from PIL import Image
from flask_sqlalchemy import SQLAlchemy
import configs

app = Flask(__name__)
PHOTO_BASE_PATH = r'/Users/xinjiezeng/PycharmProjects/flaskProject/images/'

app.config.from_object(configs)
db = SQLAlchemy(app)


class Photo(db.Model):
    __tablename__ = 'photo'
    photo_id = db.Column(db.INTEGER, primary_key=True)
    address = db.Column(db.String(50))


@app.route('/compareface', methods=['GET', 'POST'])
def compare_two_face():
    reply = compare_face()
    return reply


@app.route('/addphoto', methods=['POST'])
def add_face():

    file = request.files["file"]
    filename = request.form.get("filename")

    img = file.read()
    byte_stream = io.BytesIO(img)
    image = Image.open(byte_stream)

    save_photo_in_database(image, filename)

    return "success"


def save_photo_in_database(image, filename):
    photo = Photo(address=filename)
    db.session.add(photo)
    db.session.commit()
    image.save(PHOTO_BASE_PATH + filename)


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
