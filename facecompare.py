import urllib.request
import urllib.error
import time
from flask import json
import os


def compare_face(face_token_1, face_token_2):
    http_url = 'https://api-cn.faceplusplus.com/facepp/v3/compare'
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
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'face_token1')
    data.append(face_token_1)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'face_token2')
    data.append(face_token_2)
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
        resp = urllib.request.urlopen(req, timeout=500)
        # get response
        qrcont = resp.read()
        # if you want to load as json, you should decode first,
        # for example: json.loads(qrount.decode('utf-8'))
        reply = qrcont.decode('utf-8')

        data = json.loads(reply)
        if int(data["confidence"]) >= int(data['thresholds']['1e-4']):
            print('{"result": True, "msg": "same people"}')
            return "success"
        else:
            print('{"result": False, "msg": "different people"}')
            return "fail"

    except urllib.error.HTTPError as e:
        print(e.read().decode('utf-8'))
        return e.read().decode('utf-8')
