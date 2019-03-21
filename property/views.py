from django.shortcuts import render
# from .models import Question
from django.db.models import Q
import time, json
from django.http import JsonResponse, QueryDict, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from . import models, wx
from .utils import PropertyJSONEncoder, nonce
from dwebsocket.decorators import accept_websocket
from django.conf import settings
import os


@csrf_exempt
def dealwith(request):
    '''ceshi'''

    intent = request.GET.get("intent")
    tech = request.GET.get("tech")
    key = request.GET.get("key")
    intentId = request.GET.get("intentId")
    answerType = request.GET.get("answerType")
    question = request.GET.get("question")

    if answerType == 1:
        # question = models.Question.objects.filter(intent=intent)
        pass
    else:
        q1 = Q(intentId=intentId)
        q2 = Q(key=key)
        answers = models.Answer.objects.filter(q1 & q2)
        if answers:
            print(answers, type(answers))
            for ans in answers:
                print(ans, type(ans))
                answer = ans.answerTxt
                print(answer)
        else:
            answer = '抱歉，我没明白您的意思'

    # models.Record.objects.create(intent=intent, tech=tech, questionStr=question, answerStr=answer)
    res = {
        'code': 9000,
        'answer': answer
    }
    return JsonResponse(res)


from hashlib import md5
from itertools import permutations
from string import ascii_letters, digits
from time import time

all_letters = ascii_letters + digits + '.,;'


@accept_websocket
def test(request):
    res = {
        'code': 9000,
        'data': '数据',
        'msg': 'succese'
    }
    if not request.is_websocket():
        print('这里写实现http连接逻辑')
    else:
        print('这里实现wbsocket连接逻辑')
        print(request, request.websocket)
        for info in request.websocket:
            # info = info.decode()
            print(info, type(info))
            if info==None:
                pass
            else:
                # print(type(info.decode()), info.decode())
                print(str(time()))
                filepath = f"{settings.MEDIA_ROOT}ceshiyuyin.m4a"
                filepath = filepath.replace('\\', '/')
                # filepath = filepath.replace('//', '/')
                filepath1 = filepath.replace('.m4a', '.wav')
                print(filepath, filepath1)
                with open(filepath, 'wb') as f:
                    print(info, type(info))
                    f.write(info)
                os.system(f'ffmpeg -i {filepath} {filepath1}')
                # request.websocket.send('服务端返回信息'.encode('utf-8')+info)
                request.websocket.send(json.dumps(res))
        # return JsonResponse(res)


from dwebsocket import require_websocket, accept_websocket
import dwebsocket


@require_websocket  # 只接受websocket请求，不接受http请求，这是调用了dwebsocket的装饰器
def websocket_test(request):
    message = request.websocket.wait()
    request.websocket.send(message)


@accept_websocket  # 既能接受http也能接受websocket请求
def echo(request):
    if not request.is_websocket():
        try:
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request, 'app02/user2.html')
    else:
        for message in request.websocket:
            print(message)
            request.websocket.send(message + '这是你发来的。。。'.encode('utf-8'))
