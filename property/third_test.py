import requests, sys
import re, json, urllib.parse
import time
import hashlib
import base64
import struct

'''
测试完成：语音合成可用(文字转语音)
===   完成封装
'''

# 222.93.234.230

class SpeechSynthesis(object):
    # def __init__(cls):
    # URL = "https://openapi.xfyun.cn/v2/aiui"
    URL = "http://api.xfyun.cn/v1/service/v1/tts"
    AUE = "raw"
    APPID = "5baa012a"
    API_KEY = "5321d3eb98067a77ceb59147e6f0201c"
    # TEXT = "中秋节天气，习近平强调，改革开放以来，党中央一直关心支持爱护民营企业。我们毫不动摇地发展公有制经济，也毫不动摇地支持、保护、扶持民营经济发展、非公有制经济发展。民营企业要进一步增强信心。我们要为民营企业营造好的法治环境，进一步优化营商环境。总之，党的路线方针政策是有益于、有利于民营企业发展的"
    # TEXT = input('这里是要回复的内容')

    def getHeader(cls):
        print('get_headers')
        curTime = str(int(time.time()))
        # param = "{\"aue\":\""+AUE+"\",\"auf\":\"audio/L16;rate=16000\",\"voice_name\":\"xiaoyan\",\"engine_type\":\"intp65\"}"
        param = {
            # "scene": "main",
            "aue": "raw",
            "auf": "audio/L16;rate=16000",
            # "sample_rate": "16000",
            # "voice_name": "x_xiaoxue",
            "voice_name": "aisjinger",
            # "voice_name": "xiaoyan",
            # "pers_param": "{\"auth_id\":\"2049a1b2fdedae553bd03ce6f4820ac4\"}",
            # "data_type": "audio",
            # "auth_id": "4e925622511849a03e55a844501db949",
            "engine_type": "x"   #在线翻译， 离线设置为local
        }
        param = json.dumps(param)
        param = param.encode('utf8')
        paramBase64 = base64.b64encode(param)
        paramBase64 = paramBase64.decode('utf8')
        m2 = hashlib.md5()
        m2.update((cls.API_KEY + curTime + paramBase64).encode('utf8'))
        checkSum = m2.hexdigest()
        header ={
                'X-CurTime': curTime,
                'X-Param': paramBase64,
                'X-Appid': cls.APPID,
                'X-CheckSum': checkSum,
                # 'X-Real-Ip': '222.93.234.230',
                'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        }
        return header

    def getBody(cls, text):
        print('get_body')
        data = {'text': text}
        body_urlencode = urllib.parse.urlencode(data)
        body_utf8 = body_urlencode.encode('utf8')
        return body_utf8

    def writeFile(cls, file, content):
        print('write_file')
        with open(file, 'wb') as f:
            f.write(content)
        # f.close()
    
    def main(cls, text):
        print('main')
        r = requests.post(cls.URL,headers=cls.getHeader(), data=cls.getBody(text))
        contentType = r.headers['Content-Type']
        # print(r.text)
        # print(contentType)
        if contentType == "audio/mpeg":
            sid = r.headers['sid']
            if cls.AUE == "raw":
                cls.writeFile("static/audio/"+text+".wav", r.content)
                # cls.writeFile("audio/"+sid+".wav", r.content)
                return "static/audio/"+sid+".wav"
            else:
                cls.writeFile("static/audio/"+sid+".mp3", r.content)
                print("success, sid = " + sid)
                return "static/audio/"+sid+".mp3"
        else:
            print(r.text, '错误')


if __name__ == '__main__':
    a = SpeechSynthesis()
    a.main('这里写需要转换为语音的文字！')


