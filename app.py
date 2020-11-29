from flask import Flask, render_template, request, jsonify, json
from facedetect import detect_face
from facecompare import compare_face
from flask_mysqldb import MySQL
import os
from urllib.request import urlopen
import json


app = Flask(__name__)

app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')
app.config['API_KEY'] = os.environ.get('API_KEY')
app.config['API_SECRET'] = os.environ.get('API_SECRET')


mysql = MySQL(app)


@app.route('/')
def main():
    cursor = mysql.connection.cursor()
    user_name = ("xinjie",)
    user_id = cursor.execute("""SELECT user_id from users where username = %s""", user_name)

    cursor.execute("""SELECT face_token from faces where user_id = %s""", (user_id,))
    data = cursor.fetchall()
    cursor.close()
    return "hello"


@app.route('/login', methods= ['POST'])
def index():
    print(request.is_json)
    content = request.get_json()
    print(content)

    username = content['username']
    password = content['password']

    cursor = mysql.connection.cursor()
    user_name = (username,)
    user_id = cursor.execute("""SELECT user_id from users where username = %s""", user_name)
    user = cursor.fetchall()

    if not user:
        cursor.close()
        return "invalid"

    cursor.execute("""SELECT password from credentials where user_id = %s and password = %s""", (user_id, password,))
    data = cursor.fetchall()
    cursor.close()

    if not data:
        return "invalid"

    return "successful"



@app.route('/compareface', methods=['GET', 'POST'])
def compare_two_face():
    reply = compare_face()
    return reply




@app.route('/detectface', methods=['GET', 'POST'])
def get_face_token():
    # 把后台的数据返回到前台
    reply = detect_face()
    return reply['face_token']


if __name__ == '__main__':
    app.run(debug=True, host="192.168.254.73")

