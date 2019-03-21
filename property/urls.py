from django.urls import path

from . import api
from . import views

# 路由中使用的应用名称
app_name = 'property'

urlpatterns = [
    # 前端接口
    path('api/login/', api.login),
    path('api/register/', api.register),
    path('api/question/', api.question),
    path('api/aiui/', api.aiui),
    # path('api/answer/', api.answer)
    path('api/skilltest/', api.skillTest),
    path('api/skilltest1/{{username}}', api.skillTest1),
    path('api/map/', api.map),
    path('api/vicinity/', api.listTest),
    # path('api/del', api.delete),

    # 需要一个question语音文件路径， 返回-->文字question、answer， 语音answer文件路径
    path('api/aiui1/', api.aiui1),

    # 后台接口
    path('views/dealwith/', views.dealwith),
    path('views/socket/', views.test),

    path('views/socket/', views.test),
    path('views/websocket/', views.websocket_test),
    path('views/echo/', views.echo)
]
