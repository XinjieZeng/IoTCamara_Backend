import urllib.request
import urllib.error
import time
from flask import json
import os


def compare_face():
    http_url = 'https://api-cn.faceplusplus.com/facepp/v3/compare'
    key = os.environ.get("API_KEY")
    secret = os.environ.get("API_SECRET")
    token1 = "47ca871ce04f367fa099d542b90aeb9d"
    token2 = "4e79e2d1e33b44fa5ce6bedf25e4e338"

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
    data.append(token1)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'face_token2')
    data.append(token2)
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
            return {"result": True, "msg": "same people"}
        else:
            return {"result": False, "msg": "different people"}

    except urllib.error.HTTPError as e:
        print(e.read().decode('utf-8'))
        return e.read().decode('utf-8')
