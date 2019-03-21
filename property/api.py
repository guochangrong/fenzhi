import urllib.request, urllib.parse
import logging, os, hashlib, json, time

from django.conf import settings
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.utils import IntegrityError
from django.http import JsonResponse, QueryDict, HttpResponse
from django.utils import timezone
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.core.cache import cache

from pydub import AudioSegment
from . import models, wx
from .utils import PropertyJSONEncoder
import functools
# import demjson
from .AIUI_test import AIUI
from . import translate_test
from .third_test import SpeechSynthesis
from .semantic import get_keywordIDs
from .utils import PropertyJSONEncoder, nonce
from .decorators import ajax_login_required


# def api(func):
#     @functools.wraps(func)
#     def _deal_with(request, *args, **kwargs):
#         response_data = demjson.encode(func(request, *args, **kwargs))
#         response = HttpResponse(demjson.encode(response_data), content_type="application/json")
#         response["Access-Control-Allow-Origin"] = "*"
#         response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
#         response["Access-Control-Max-Age"] = "1000"
#         response["Access-Control-Allow-Headers"] = "*"
#         return response
#     return _deal_with


@csrf_exempt
def question(request):
    '''这里是获得语音文件路径（暂时写死）'''
    filepath = request.POST.get('filepath')
    # print(filepath)
    # filepath = 'C:/Users/gcr/PycharmProjects/xytproperty/property/audio/hts002d7f80@ch159c0f191b1a477400.wav'

    '''这里写语音转文字'''
    ques = translate_test.main(filepath)

    # print(qs)
    res = {
        'code': 9000,
        'data': ques['data']
    }
    return JsonResponse(res)


@csrf_exempt
def aiui(request):

    '''这里是获取的参数（暂时用input代替）'''
    # text1 = input('客户输入问题')
    if request.method == 'POST':
        # for key in request.POST:
        #     print(key)
        text2 = request.POST.get('question')
        print(text2)
        a = AIUI()

        data = a.main(text2)
    else:
        data = '感谢您的咨询'

    res = {
        'code': 9001,
        'data': data
    }
    return JsonResponse(res)


# @csrf_exempt

def skillTest2(file):
    '''测试新建技能'''
    # http://192.168.0.107:8000/api/skilltest/
    # file = request.FILES.get('wxfile')
    filepath = f"{settings.MEDIA_ROOT}{file.name}"
    filepath = filepath.replace('\\', '/')
    filepath1 = filepath.replace('.m4a', '.wav')
    print(filepath, filepath1)
    with open(filepath, 'wb') as f:
        for fiaudio in file.chunks():
            # print(fiaudio, type(fiaudio))
            f.write(fiaudio)

    os.system(f'ffmpeg -i {filepath} {filepath1}')
    ques = translate_test.main(filepath1)
    print(ques)
    os.remove(filepath)
    os.remove(filepath1)

    return ques['data']


def AIUI_deal(ques, openid):
    a = AIUI()
    # answer = a.main(ques)
    data = a.main(ques, openid)
    print(data)
    try:
        answer = data['intent']['answer']['text']
        print('runing Try')
        # print(data['intent'].get('semantic')[0]['slots'])
        normValue = data['intent'].get('semantic')[0]['slots'][0]['normValue']
        print('runing Try1')
        value = data['intent'].get('semantic')[0]['slots'][0]['value']
        tech = data['intent'].get('service')
        intent = data['intent'].get('semantic')[0].get('intent')
        if answer == value:
            answer = normValue
        else:
            pass
    except:
        print(data, type(data), '123456987')
        # if data != '识别失败':
        if data['intent']['answer']['text']:
            answer = data['intent']['answer']['text']
            tech = '我的问答'
        else:
            answer = '识别失败'
            tech = ''
        intent = ''
        normValue = ''
        value = answer

    res = {
        'answer': answer,
        'tech': tech,
        'intent': intent,
        'normValue': normValue,
        'value': value,
    }
    return res


@csrf_exempt
@ajax_login_required
def aiui1(request):

    user = request.user
    # 此处可以考虑用缓存
    if cache.has_key(f'{user.id}'):
        userprofile = cache.get(f'{user.id}')
        print('从缓存中获得客户数据', userprofile)
    else:
        userprofile = models.UserProfile.objects.get(user_id=user.id)
        cache.set(f'{user.id}', userprofile, 60*30)
        print('缓存客户数据')
    # userprofile = models.UserProfile.objects.get(user_id=user.id)
    openid = userprofile.openId

    # 将openid通过md5加密， 转换成auth_id
    m = hashlib.md5()
    m.update(openid.encode("utf8"))
    auth_id = m.hexdigest()
    print(openid, type(openid))
    print(auth_id, type(auth_id))

    '''这里是获取的参数'''
    if request.method == 'POST':
        file = request.FILES.get('wxfile')
        ques = skillTest2(file)
        # for key in request.POST:
        #     print(key)
        # text2 = request.POST.get('question')
        # print(text2)
        # filepath = request.POST.get('filepath')
        # filepath = request.GET.get('filepath')
        # print(filepath)

        # '''通过语音识别接口，实现question语音转文字'''
        # ques = translate_test.main(filepath)
        # ques = ques.get('data')
        # # ques = text2
        # print(ques)

        # '''用input标签输入测试问题
        # '''
        # ques = input('输入问题')
        #
        # '''数据库操作'''
        # # q_question = Q(question__content=ques)
        # # answers = models.Answer.objects.filter(content='今天北京天气晴朗， 适合外出')
        # # print(answers, type(answers))
        # answers = models.Answer.objects.filter(question__content=ques)
        # if answers:
        #     # answers = models.Answer.objects.all()
        #     print(answers, type(answers))
        #     for ans in answers:
        #         # print(type(ans))
        #         answer = ans.content
        #         print(ans.content, type(ans.content))
        #         ques = ans.question.content
        #         print(ans.question.content)
        #         answerPath = ans.path
        #         print(ans.path)
        #     # answer =
        #
        # else:

            # '''通过语义理解接口， 获得问题关键字'''
            # c = get_keywordIDs(ques)
            # print(c, type(c))
            #
            # city = c.get('city')
            # userName = c.get('userName')
            # print(city, userName)

            # '''没有原版问题，试通过条件判断寻找相似问题，返回答案'''
            # if city:
            #     answers = models.Answer.objects.filter(question__city=city)
            #     print(answers)
            #     for ans in answers:
            #         answer = ans.content
            #         print(answer)

        '''通过AIUI接口实现智能回答， 获得文字answer'''

        try:
            cache.get('ending')
            # last_answer = cache.get('ending')
            # print('缓存中的ending', last_answer)
            if ques == ('不用了' or '没有了') and cache.get('ending') != None:
            # if ques == '不用了' or ques =='没有了':
            #     print('ques', ques, type(ques))
            #     print('走到这里了')
                answer = '感谢咨询'
                tech = ''
                intent = ''
            else:
                ans_data = AIUI_deal(ques, auth_id)
                answer = ans_data.get('answer')
                tech = ans_data.get('tech')
                intent = ans_data.get('intent')
                normValue = ans_data.get('normValue')
                value = ans_data.get('value')
                if answer == '是否介绍':
                    cache.set('ending', answer, 60)
        except:
            ans_data = AIUI_deal(ques, auth_id)
            answer = ans_data.get('answer')
            tech = ans_data.get('tech')
            intent = ans_data.get('intent')
            normValue = ans_data.get('normValue')
            value = ans_data.get('value')
            # if answer == '是否介绍':
            if '是否介绍' in answer:
                cache.set('ending', answer, 60*3)
            # a = AIUI()
            # # answer = a.main(ques)
            # data = a.main(ques)
            # print(data)
            # try:
            #     answer = data['intent']['answer']['text']
            #     print('runing Try')
            #     # print(data['intent'].get('semantic')[0]['slots'])
            #     normValue = data['intent'].get('semantic')[0]['slots'][0]['normValue']
            #     print('runing Try1')
            #     value = data['intent'].get('semantic')[0]['slots'][0]['value']
            #     tech = data['intent'].get('service')
            #     intent = data['intent'].get('semantic')[0].get('intent')
            #     if answer == value:
            #         answer = normValue
            #     else:
            #         pass
            # except:
            #     answer = data['intent']['answer']['text']
            #     tech = '我的问答'
            #     intent = ''
        try:
            # q1 = Q(intentid=intent)
            q2 = Q(key=answer)
            print(f'数据库搜索, key:{answer}')
            answers = models.Answer.objects.filter(q2)
            for ans in answers:
                print(ans, type(ans))
                answer = ans.answerTxt
                answerPath = ans.answerAudio
                # print(answer)
        except:
            answer = answer

            '''通过语音合成接口， 实现answer文字转语音'''
            b = SpeechSynthesis()
            answerPath = b.main(answer)
            answerPath = os.path.join(settings.BASE_DIR, answerPath)
            print(answerPath)

        '''存储流水表'''
        models.Record.objects.create(intent=intent, tech=tech, userId=user.id, questionStr=ques, answerStr=answer)

            # '''将新的问题和答案存入数据库'''
            # ques_obj = models.Question.objects.create(content=ques, city=city)
            # models.Answer.objects.create(content=answer, path=answerPath, question=ques_obj)
        # models.Record.objects.create(answerStr=answer, questionStr=ques)
    else:
        ques = 'http://226cj31961.iok.la/static/audio/识别失败.wav'
        answer = '识别失败'
        answerPath = "http://226cj31961.iok.la/static/audio/111319.m4a"

    res = {
        'code': 9001,
        'data': [{
            'ques': ques,  # 返回文字question
            'answer': answer,  # 返回文字answer
            # 'answerPath': answerPath,  # 返回语音answer文件路径
            'fpath': answerPath
        }],
    }
    return JsonResponse(res, json_dumps_params={'ensure_ascii': False})


def login(request):
    """自动登录"""

    # 通过code获取openid
    code = request.GET.get('code')
    wx_session = wx.fetch_session(code)
    print('wx_session', wx_session)

    res = {
        'code': 9000,
        'message': _('Success'),
    }

    if 'openid' in wx_session:
        # 通过openid在数据库中查找用户
        users = list(models.UserProfile.objects.filter(openId=wx_session['openid']))
        if len(users):
            print(users, users[0])
            user_id = users[0].user_id
            user = models.User.objects.get(id=user_id)
            # user = users[0]
            # 暴力退出并登录新user
            django_logout(request)
            django_login(request, user)
            # 将用户信息返回给小程序
            res['data'] = users[0]
        else:
            res['code'] = 9009
            res['message'] = _('Unauthorized')
            res['data'] = wx_session['openid']
    else:
        res['code'] = 9010
        res['message'] = wx_session['errmsg']

    return JsonResponse(res, encoder=PropertyJSONEncoder)


@csrf_exempt
def register(request):
    """用户授权一键注册并登录"""

    nickname = request.POST.get('nickname')
    sex = request.POST.get('sex')
    openid = request.POST.get('openid')
    avatar = request.POST.get('avatar')
    time_now = timezone.now()

    try:
        user_profile = models.UserProfile.objects.get(openId=openid)
        user_id = user_profile.user_id
        # user = models.User.objects.get(id=user_id)
        if not user_id:
            raise ObjectDoesNotExist()
        else:
            user = models.User.objects.get(id=user_id)
    except ObjectDoesNotExist:

        # 将微信头像下载到自己的服务器上
        filename = nonce()
        local_avatar = '%suser/%s.png' % (settings.MEDIA_ROOT, filename)
        urllib.request.urlretrieve(avatar, filename=local_avatar)
        avatar = 'user/%s.png' % (filename,)

        # 计算有效期
        # start_date = timezone.now()
        # end_date = start_date.replace(month=start_date.month + 6)

        # 创建Django用户
        try:
            print('创建Django用户')
            user = User.objects.create_user(nickname, password=openid)
            print(type(user))
            q1 = Q(username=nickname)
            q2 = Q(password=openid)
            user1 = models.User.objects.filter(q1 | q2)
            print(user1, '123')
            for u in user1:
                print(u, u.id, '456')
                user_id = u.id
        except IntegrityError:
            # 如果用户名相同，则在用户名后添加随机字符串再次创建
            nickname = nickname + '_' + filename
            user = User.objects.create_user(nickname, password=openid)
            q1 = Q(username=nickname)
            q2 = Q(password=openid)
            user1 = models.User.objects.filter(q1 | q2)
            print(user1, '1233')
            for u in user1:
                print(u, u.id, '4566')
                user_id = u.id


        # 创建用户资料

        user_profile = models.UserProfile.objects.create(user_id=user_id, nickname=nickname, sex=sex, openId=openid, avatar=avatar, last_login=time_now, status=2)

    # 暴力退出并重新登录新user
    django_logout(request)
    django_login(request, user)

    # 返回用户信息
    res = {
        'code': 9000,
        'message': _('Success'),
        'data': user_profile
    }

    return JsonResponse(res, encoder=PropertyJSONEncoder)


@csrf_exempt
@ajax_login_required
def skillTest(request):
    '''测试新建技能'''
    user = request.user
    # 此处可以考虑用缓存
    print('测试缓存')
    print(user.id, type(user))
    if cache.has_key(f'{user.id}'):
        userprofile = cache.get(f'{user.id}')
        print('客户数据', userprofile, type(userprofile))
        print('客户userID', userprofile.id, 'openID', userprofile.openId)
    else:
        userprofile = models.UserProfile.objects.get(user_id=user.id)
        print(userprofile)
        print(userprofile.id, userprofile.openId, userprofile.nickname, userprofile.sex, userprofile.avatar, userprofile.last_login)
        cache.set(f'{user.id}', userprofile, 60*30)
        print('缓存客户数据')
    res = {
        'data': '服务端数据',
        'code': 9000,
    }
    return JsonResponse(res, json_dumps_params={'ensure_ascii': False})


from dwebsocket.decorators import accept_websocket
import threading

clients = {}

@accept_websocket
def skillTest1(request, username):
    # 测试socket
    print('999')
    count = 0

    if request.is_websocket:
        lock = threading.RLock()
        try:
            lock.acquire()#抢占资源
            s = {}
            if clients.get(username) != None:
                s[str(request.websocket)] = request.websocket
            else:
                count += 1
                s[str(request.str(request.websocket))] = request.websocket
                clients[username] = s
            print('用户人数', str(count))

            for message in request.websocket:
                if not message:
                    break
                else:
                    request.send(message)
        except:
            pass
        finally:
            # 通过用户名找到 连接信息 再通过 连接信息 k 找到 v (k就是连接信息)
            clients.get(username).pop(str(request.websocket))
            # 释放锁
            lock.release()

# 发送消息
def websocketMsg(client, msg):
    import json
    # 因为一个账号会有多个页面打开 所以连接信息需要遍历
    for cli in client:
        'client客户端 ，msg消息'
        b1 = json.dumps(msg).encode('utf-8')
        client[cli].send(b1)


# 服务端发送消息
def send(username, title, data, url):
    'username:用户名 title：消息标题 data：消息内容，消息内容:ulr'
    try:
        if clients[username]:
            websocketMsg(clients[username], {'title': title, 'data': data, 'url': url})
            # 根据业务需求 可有可无    数据做 持久化
            # messageLog = MessageLog(name=username, msg_title=title, msg=data, msg_url=url, is_required=0)

            flg = 1
        flg = -1
    except BaseException:
        # messageLog = MessageLog(name=username, msg_title=title, msg=data, msg_url=url, is_required=1)
        pass
    finally:
        pass


# def delete(request):
#     models.Record.objects.filter(answerStr='识别失败').delete()
#     return JsonResponse({'msg': '删除成功'})

def map(request):
    # print('123')
    # location = request.GET.get('location')
    # print(location)
    # location1 = urllib.parse.quote(location)
    # 地图接口秘钥（可自己自行申请）
    myKey = 'BEKBZ-FWSKG-ZJCQX-ILO4A-W74HE-H4BUD'
    # 项目所在经纬度
    projectCoordinate = '31.2900250000,120.5982340000'
    # res = urllib.request.urlopen('https://apis.map.qq.com/ws/geocoder/v1/?address=%s&key=BEKBZ-FWSKG-ZJCQX-ILO4A-W74HE-H4BUD' % ('%E8%8B%8F%E5%B7%9E%E7%81%AB%E8%BD%A6%E7%AB%99'))
    # res = urllib.request.urlopen('https://apis.map.qq.com/ws/geocoder/v1/?address=%s&key=%s' % (location1, myKey))

    # json_result = res.read().decode('utf8')
    # json_result = json.loads(json_result)
    # print(json_result, '地图数据', type(json_result))
    # lat = json_result['result']['location']['lat']
    # lng = json_result['result']['location']['lng']
    # ll = str(lat) + ',' + str(lng)
    # print(ll)

    '''获取特定地址与项目之间距离（步行/驾车）'''

    # 获取计算距离（步行/驾车）方式
    a = request.GET.get('mode') if request.GET.get('mode') else 'walking'
    print(a)
    b = models.Vicinity.objects.get(projectName='龙湖天赋')
    vicinityData = b.vicinityData
    data = vicinityData.get('data')
    # print(data)
    for key, value in data.items():
        print(key, value)
        for idx, d in enumerate(value):
            print(d, d.get('lat'), d.get('lng'))
            ll = str(d.get('lat')) + ',' + str(d.get('lng'))
            data.get(key)[idx]['id'] = idx

            res = urllib.request.urlopen(
                'https://apis.map.qq.com/ws/distance/v1/?mode=%s&from=%s&to=%s&key=%s' % (a, projectCoordinate, ll, myKey))
            json_result1 = res.read().decode('utf8')
            json_result1 = json.loads(json_result1)
            print(json_result1, '地图数据1', type(json_result1))
            # # json_result1 = json.dumps(json_result1)
            # print('距离: ', json_result1.get('result').get('elements')[0].get('distance'))
            a1 = '步行' if a == 'walking' else ('驾车' if a == 'driving' else '')
            distance = a1 + '距离:' + str(json_result1.get('result').get('elements')[0].get('distance')) + '米'
            # print(distance)
            data.get(key)[idx]['distance1'] = distance
            time.sleep(0.3)


    # print(data)
    vicinityData.data = data
    # print("调整后周边数据", vicinityData)
    models.Vicinity.objects.filter(projectName='龙湖天赋').update(vicinityData=vicinityData)


    re = {
        'code': 9000,
        'location': '龙湖天赋',
        # 'data': {
        #     'destination': location,
        #     'lat': json_result['result']['location']['lat'],
        #     'lng': json_result['result']['location']['lng'],
        #     # 'distance': distance
        # }
    }
    # vicinity = models.Vicinity.objects.create(projectName=res['location'], vicinityData=res, status=-2)
    return JsonResponse(re)


def listTest(request):
    print('项目周边数据接口测试')
    b = models.Vicinity.objects.get(projectName='龙湖天赋')
    # print(b, b.projectName, b.vicinityData, type(b.vicinityData))

    return JsonResponse(b.vicinityData)
