#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
# import urllib.parse
# import urllib.request
from urllib import parse, request
import json
import hashlib
import base64

'''
已实现语音转文字
'''

def main(filepath):
    # f = open("audio/hts00155bb9@ch79490f08d48e477500.wav", 'rb')
    f = open(filepath, 'rb')
    file_content = f.read()
    base64_audio = base64.b64encode(file_content).decode('utf8')
    body = parse.urlencode({'audio': base64_audio}).encode('utf8')

    url = 'http://api.xfyun.cn/v1/service/v1/iat'
    api_key = '5a22f9d7a772e8e28ca3838ae3b18bae'
    param = {"engine_type": "sms16k", "aue": "raw"}

    x_appid = '5baa012a'
    x_param = base64.b64encode(json.dumps(param).replace(' ', '').encode('utf8'))
    x_param = x_param.decode('utf8')
    x_time = int(int(round(time.time() * 1000)) / 1000)
    # x_time = int(time.time())
    x_checksum = hashlib.md5((api_key + str(x_time) + x_param).encode('utf8')).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': str(x_time),
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    # req = urllib.request(url, body, x_header)
    # result = urllib.parse.urlopen(req)
    req = request.Request(url=url, data=body, headers=x_header, method='POST')
    result = request.urlopen(req)
    result = result.read().decode('utf8')
    print(result, type(result))
    result = json.loads(result)
    print(result['data'])
    return result

if __name__ == '__main__':
    main('C:/Users/gcr/Desktop/临时保存/tmp_e2dc5d54607d3b3e538b90f8b4daa1b79fb2fb36a1c3c509.wav')