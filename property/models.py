from django.db import models
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# from django.utils.translation import ugettext_lazy as _
import mongoengine
# from xytproperty.settings import DBNAME
from mongoengine import *
from djongo import models
# connect("xyt_sales")


# class Question(Document):
#     STATUS = (
#                 (2, _('Enabled')),
#                 (-2, _('Disabled'))
#             )
#     status = IntField(_('Status'), default=2)
#     # name = StringField(max_length=225)
#     intent = StringField(max_length=100)
#     answerType = IntField(default=1)
#     answerMethod = IntField(default=1)
#     answerTxt = StringField(max_length=225)
#     # create_user_id = IntField(_('Create User'), null=True, editable=False)
#     # create_time = DateTimeField(_('Create Time'), default=timezone.now, editable=False)
#     create_time = DateTimeField(default=str(timezone.now))
#     # update_user_id = IntField(_('Update User'), null=True, editable=False)
#     # update_time = DateTimeField(_('Update Time'), default=timezone.now, editable=False)
#
#     @queryset_manager
#     def show_newest(doc_cls, queryset):
#         # 通过poem_id降序显示
#         return queryset.order_by('status')


# class Answer(Document):
#     meta = {
#         'key': 'poem_data'
#     }
#     STATUS = (
#         (2, _('Enabled')),
#         (-2, _('Disabled'))
#     )
#     status = IntField(_('Status'), default=2)
#     # name = StringField(max_length=225)
#     intendId = StringField(max_length=225)
#     # key | map[string]int | 槽位内容作为key |
#     # key = MapField(default=meta)
#     answerMethod = IntField(default=1)
#     answerAudio = StringField(default=None)
#     answerTxt = StringField(default=None)
#     # isDefault = BooleanField()   #是否作为此意图的默认回答
#     # create_user_id = IntField(_('Create User'), null=True, editable=False)
#     # create_time = DateTimeField(_('Create Time'), default=timezone.now, editable=False)
#     create_time = DateTimeField(default=str(timezone.now))
#     # update_user_id = IntField(_('Update User'), null=True, editable=False)
#     # update_time = DateTimeField(_('Update Time'), default=timezone.now, editable=False)


# class UserProfile(Document):
#     STATUS = (
#         (2, _('Enabled')),
#         (-2, _('Disabled'))
#     )
#     SEX = (
#                       (1, _('Male')),
#                       (2, _('Female'))
#                   )
#     status = IntField(_('Status'), default=2)
#     # id = ObjectIdField()
#     userid = StringField(max_length=100)
#     openId = StringField(max_length=20)    #微信openID
#     unionId = StringField(max_length=20)      #微信unionID
#     avatar = StringField(max_length=50)
#     # user = OneToOneField(User, on_delete=models.DO_NOTHING, null=True, verbose_name=_('User'))
#     nickname = StringField(max_length=255, default='')
#     sex = IntField(_('Sex'), choices=SEX, default=1, null=False)
#     age = models.IntegerField(_('age'), null=True)
#     # create_time = DateTimeField(_('Create Time'), default=timezone.now, editable=False)
#     create_time = DateTimeField(default=str(timezone.now))
#     # question = models.ForeignKey(Question, null=True, on_delete=models.DO_NOTHING, verbose_name=_('Question'))
#     # wx_id = models.CharField(_('Wx_id'), max_length=100, default='', editable=False)
#     #


class Base(models.Model):
    '''模型父类'''

    STATUS = (
        (2, '启用'),
        (-2, '禁用')
    )

    status = models.IntegerField('状态', default=2, choices=STATUS)
    create_user_id = models.IntegerField('创建者ID', null=True, editable=False)
    create_time = models.DateTimeField('创建时间', default=timezone.now, editable=False)
    update_user_id = models.IntegerField('更新者ID', null=True, editable=False)
    update_time = models.DateTimeField('更新时间', default=timezone.now, editable=False)

    class Meta:
        # 抽象模型，让base模型的字段融合到base的子类中,而不是分成两个表
        abstract = True

class Entry(models.Model):
    base = models.EmbeddedModelField(
        model_container=Base,
    )

    headline = models.CharField(max_length=225)


class Question(Base):
    '''客户问题'''

    intent = models.CharField(_('intent'), max_length=255, null=True)
    answerTxt = models.CharField(_('answerTxt'), max_length=255, default='')
    answerType = models.IntegerField(_('answerType'), default=1)
    answerMethod = models.IntegerField(_('answerMothod'), default=1)
    # content = models.CharField(_('content'), max_length=255, null=False)
    # city = models.CharField(_('city'), max_length=255, default='苏州')
    # position = models.CharField(_('position'), max_length=255, default='苏州')
    # area = models.CharField(_('area'), max_length=255, null=True)

    class Meta:
        verbose_name = '问题'
        verbose_name_plural = '问题'


class Answer(Base):
    '''提供回答'''

    meta = {
                'key': 'poem_data'
            }
    # content = models.CharField(_('content'), max_length=255, null=False)
    intentId = models.CharField(_('intentId'), max_length=255, null=True)
    # key | map[string]int | 槽位内容作为key |
    # key = models.DictField(_('key'), default=meta)
    key = models.CharField('关键字', max_length=100, default='')
    answerMethod = models.IntegerField('问答类型', default=1)
    answerAudio = models.CharField('语音问答', max_length=255, null=True)
    isDefault = models.BooleanField('是否为默认值', default=False)
    answerTxt = models.CharField('问题答案', max_length=500, default='')
    # question = models.ForeignKey(Question, null=True, on_delete=models.DO_NOTHING, verbose_name=_('Question'))
    # path = models.CharField(_('path'), max_length=225, null=True)

    class Meta:
        verbose_name = '问题答案'
        verbose_name_plural = '问题答案'


class Record(models.Model):
    STATUS = (
        (2, _('Enabled')),
        (-2, _('Disabled'))
    )

    status = models.IntegerField('状态', default=2, choices=STATUS)
    intent = models.CharField(_('intent'), default='', max_length=225)
    tech = models.CharField(_('tech'), default='', max_length=20)
    userId = models.CharField(_('userId'), default='', max_length=20)
    questionStr = models.CharField('问题', default='', max_length=20)
    answerStr = models.CharField('答案', default='', max_length=20)
    create_time = models.DateTimeField('创建时间', default=timezone.now, editable=False)

    class Meta:
        verbose_name = '问答记录'
        verbose_name_plural = '问答记录'

# class classEmbed(EmbeddedDocument):
#     t = StringField()
#     p = StringField()
#
#
# class Test(Document):
#     g = EmbeddedDocumentListField(classEmbed)

class UserStorage(FileSystemStorage):
    """处理用户头像"""

    def _save(self, name, content):
        filename = super()._save(name, content)

        path = self.path(name)
        from PIL import Image
        img = Image.open(path)

        left = top = right = bottom = 0
        if img.width > img.height:
            left = (img.width - img.height) / 2
            right = left + img.height
            bottom = img.height
        else:
            top = (img.height - img.width) / 2
            bottom = top + img.width
            right = img.width
        img.crop((left, top, right, bottom)).resize((200, 200), resample=Image.BICUBIC).save(path)
        return filename


class UserProfile(Base):
    '''用户资料'''

    SEX = (
        (1, _('Male')),
        (2, _('Female'))
    )

    # user = models.OneToOneField(User, on_delete=models.DO_NOTHING, null=True, verbose_name=_('User'))
    user_id = models.IntegerField(null=True)
    nickname = models.CharField('昵称', max_length=255, default='')
    sex = models.IntegerField('性别', choices=SEX, default=1)
    openId = models.CharField(max_length=100, default='')
    # unionId = models.CharField(max_length=100, default='')
    avatar = models.ImageField('头像', upload_to='user', blank=True, storage=UserStorage(), null=True)
    last_login = models.DateTimeField('上次登录', null=True)
    # lastIp = models.CharField(_('lastIp'), default='', max_length=20)
    # g = ListField(DictField(Mapping.build(
    #     test1=StringField(required=True),
    #     test2=StringField(required=True)
    # )))

    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'

    # def __repr__(self):
    #     return '<UserProfile {id: %s, mobile: %s}>' % (self.id, self.mobile)
    #
    # def __str__(self):
    #     return self.user.username if self.user else self.mobile

class Vicinity(models.Model):
    STATUS = (
        (2, _('Enabled')),
        (-2, _('Disabled'))
    )

    status = models.IntegerField('状态', default=2, choices=STATUS)
    projectName = models.CharField('项目名称', max_length=255, default='')
    vicinityData = models.DictField('周边数据', default={},)
    create_time = models.DateTimeField('创建时间', default=timezone.now, editable=False)

    class Meta:
        verbose_name = '项目周边'
        verbose_name_plural = '项目周边'
