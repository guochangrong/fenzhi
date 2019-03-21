import requests
import time
import hashlib, json
import base64


class AIUI(object):

    URL = "https://openapi.xfyun.cn/v2/aiui"
    APPID = "5baa012a"
    API_KEY = "5a8b5edf85c441a482bb973022b5794c"
    # AUDIO_PATH = "audio_test.wav"
    AUDIO_PATH = "audio/hts0017c751@ch159c0f0a3e3d477400.wav"

    IP= '117.81.140.242'

    def getHeader(cls, auth_id):
        curTime = str(int(time.time()))
        # param = "{"aue":"raw","auth_id":"3154914b8a917f8d1b8fe647605f5bd8","data_type":"audio","sample_rate":"16000","scene":"main"}"
        param = {
            # "result_level":"complete",
            # "aue":"raw",
            # "auth_id":"3154914b8a917f8d1b8fe647605f5bd8",
            "auth_id": auth_id,
            # "data_type":"audio",
            "data_type":"text",
            # "sample_rate":"16000",
            "scene":"main",
            # "lat":"39.26",
            # "lng":"115.14"
        }
        # paramBase64 = base64.b64encode(param)
        param = json.dumps(param)
        param = param.encode('utf8')
        paramBase64 = base64.b64encode(param)
        paramBase64 = paramBase64.decode('utf8')

        m2 = hashlib.md5()
        m2.update((cls.API_KEY + curTime + paramBase64).encode('utf8'))
        checkSum = m2.hexdigest()

        header = {
            'X-CurTime': curTime,
            'X-Param': paramBase64,
            'X-Appid': cls.APPID,
            'X-CheckSum': checkSum,
        }
        # print(header)
        return header



    def getBody(cls, filepath):
        binfile = open(filepath, 'rb')
        data = binfile.read()
        # print(data)
        return data

    def main(cls, text1, auth_id):
        # r = requests.post(cls.URL, headers=cls.getHeader(), data=cls.getBody(AUDIO_PATH))
        # textl = "北京天气"
        # while True:
        # textl = input('输入问题')
        textl = text1.encode('utf8')
        r = requests.post(cls.URL, headers=cls.getHeader(auth_id), data=textl)
        # print(r.content)
        # print(r.text)
        r1 = json.loads(r.content)
        print(r1)
        # print(r1['data'][0]['intent'])
        try:
            # data = r1['data'][0]['intent']['answer']['text']
            data = r1['data'][0]
        except:
            data = '识别失败'
        # print(data)
        return data


# 834eb562666319d0ad8be2bb7ed101f3
# oI2sc5Pdg7eHpVnH_Jhhvf0DN1tg
# 075a8ec641647f4ba4d106e7c6ffc70a