import time
import urllib.request
import urllib.parse
import json
import hashlib
import base64
from django.http import JsonResponse


IP = '117.81.222.240'
url = '192.168.0.107:8000/api/aiui1/'


def main(model, TEXT):
    # TEXT = input('输入要分析的语句')
    body = urllib.parse.urlencode({'text': TEXT}).encode('utf-8')

    url = f'http://ltpapi.xfyun.cn/v1/{model}'
    api_key = '6e7fb0e47ea7cae9a12a4d9f65282c8b'
    param = {"type": "dependent"}

    x_appid = '5baa012a'
    x_param = base64.b64encode(json.dumps(param).replace(' ', '').encode('utf-8'))
    x_time = int(int(round(time.time() * 1000)) / 1000)
    x_checksum = hashlib.md5(api_key.encode('utf-8') + str(x_time).encode('utf-8') + x_param).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    req = urllib.request.Request(url, body, x_header)
    result = urllib.request.urlopen(req)
    result = result.read()
    result = result.decode('utf-8')
    result = json.loads(result)
    # print(type(result), result.get('data'))
    return result


def get_keywordIDs(TEXT):
    keywordIDs = {}
    result = main('pos', TEXT)
    # if model == 'pos':
    print(result, type(result))
    print(result.get('data')['pos'])
    genres = result.get('data')['pos']
    for id, genre in enumerate(genres):
        # print(id, genre)
        if genre == 'nh':
            userName_id = id
            keywordIDs['userName_id'] = userName_id
        elif genre == 'ns':
            city_id = id
            keywordIDs['city_id'] = city_id
        else:
            pass
    # print(keywordIDs)
    a = get_keywords(TEXT, keywordIDs)
    print(a)
    return a
    # elif model == 'cws':
    #     return result

def get_keywords(TEXT, keywordIDs):
    keywords = {}
    result = main('cws', TEXT)
    # result = a.get('data')['word']
    words = result.get('data')['word']
    # print(words, type(words))
    # print(keywordIDs, type(keywords))
    city_id = keywordIDs.get('city_id')
    userName_id = keywordIDs.get('userName_id')
    # print('获得关键字id', city_id, userName_id)
    if city_id != '0' or city_id == '0':
        # print('获得城市')
        city_id = int(city_id)
        # print(city_id)
        city = words[city_id]
        # print('城市：', city)
        keywords['city'] = city
    if userName_id:
        userName_id = int(userName_id)
        userName = words[userName_id]
        # print('用户名：', userName)
        keywords['userName'] = userName
    # print('关键字：', keywords)
    return keywords


if __name__ == '__main__':
    # main()
    # while True:
    #     models = ['cws', 'pos', 'ner', 'dp', 'srl', 'sdp']
    #     TEXT = input('输入问题： ')
    #     time1 = time.time()
    #     for x in range(6):
    #         url = models[x]
    #         main(url, TEXT)
    #     timeload = time.time() - time1
    #     print(timeload)

    TEXT = input('输入问题：')
    get_keywordIDs(TEXT)
