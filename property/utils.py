import random

from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.fields.files import ImageFieldFile

from . import models


class PropertyJSONEncoder(DjangoJSONEncoder):
    '''统一JSON序列化'''

    def default(self, obj):
        if isinstance(obj, ImageFieldFile):
            return obj.url
        if isinstance(obj, models.Question):
            return dict([
                (attr, getattr(obj, attr)) for attr in [
                    'id', 'intent', 'answerTxt', 'answerType', 'answerMethod'
                ]
            ])
        elif isinstance(obj, models.Answer):
            return dict([
                (attr, getattr(obj, attr)) for attr in [
                    'id', 'intentId', 'key', 'answerMethod', 'answerAudio', 'isDefault', 'answerTxt'
                ]
            ])
        elif isinstance(obj, models.UserProfile):
            return dict([
                (attr, getattr(obj, attr)) for attr in [
                    'id', 'nickname', 'sex', 'avatar', 'last_login'
                ]
            ])
        elif isinstance(obj, models.Vicinity):
            return dict([
                (attr, getattr(obj, attr)) for attr in [
                    'id', 'projectName', 'vicinityData', 'states'
                ]
            ])
        elif isinstance(obj, User):
            return dict([
                (attr, getattr(obj, attr)) for attr in [
                    'id', 'username', 'first_name', 'email'
                ]
            ])
        else:
            return super().default(obj)


def nonce(length=10):
    """随机字符串"""

    return ''.join(random.sample(list('abcdefghijklmnopqrstuvwxyz0123456789'), length))
