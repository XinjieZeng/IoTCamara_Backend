# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import time
import json

PHOTO_BASE_PATH = r'/Users/xinjiezeng/PycharmProjects/flaskProject/images/'


def detect_face(img):
    http_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    # key = os.environ.get("API_KEY")
    # secret = os.environ.get("API_SECRET")
    key = "vTLWlxe8ooTcPutTopW624ANrOthhNeh"
    secret = "yD118XLLTEaJCh4N2Zzs0XzJHViobsFL"

    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
    data.append(key)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
    data.append(secret)
    data.append('--%s' % boundary)
    # fr = open(PHOTO_BASE_PATH+path, 'rb')
    data.append('Content-Disposition: form-data; name="%s"; filename=" "' % 'image_file')
    data.append('Content-Type: %s\r\n' % 'application/octet-stream')
    # print(img)
    data.append(img)
    # data.append(fr.read())
    # print(fr.read())
    # fr.close()
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_landmark')
    data.append('1')
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_attributes')
    data.append(
        "gender,age,smiling,headpose,facequality,blur,eyestatus,emotion,ethnicity,beauty,mouthstatus,eyegaze,skinstatus")
    data.append('--%s--\r\n' % boundary)

    for i, d in enumerate(data):
        if isinstance(d, str):
            data[i] = d.encode('utf-8')

    http_body = b'\r\n'.join(data)

    # build http request
    req = urllib.request.Request(url=http_url, data=http_body)

    # header
    req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)

    try:
        # post data to server
        resp = urllib.request.urlopen(req, timeout=5000)
        # get response
        qrcont = resp.read()
        # if you want to load as json, you should decode first,
        # for example: json.loads(qrount.decode('utf-8'))
        reply = qrcont.decode('utf-8')
        j = json.loads(reply)

        if not j["faces"]:
            raise ValueError("cannot detect the face")

        return j['faces'][0]['face_token']

    except urllib.error.HTTPError as e:
        print(e.read().decode('utf-8'))
        return e.read().decode('utf-8')
