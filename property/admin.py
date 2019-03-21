from django.contrib import admin
from django.conf import settings
from django.utils import timezone
from . import models
from .models import Entry
from django.utils.translation import gettext_lazy as _

# 站点设置
admin.site.site_header = _('Xinyutang Property Manage')
admin.site.site_title = _('Xinyutang Property Manage')
admin.site.index_title = _('Home')
admin.site.register(Entry)


def update_enabled(admin_model, request, queryset):
    """批量启用动作"""
    queryset.update(status=2)


def update_disabled(admin_model, request, queryset):
    """批量禁用动作"""
    queryset.update(status=-2)


class BaseAdmin(admin.ModelAdmin):
    """后台管理统一父类"""

    list_filter = ('status',)
    # 将动作函数添加到动作列表中
    actions = (update_enabled, update_disabled)

    def save_model(self, request, obj, form, change):
        if change:
            obj.update_user_id = request.user.id
            obj.update_time = timezone.now()
        else:
            obj.create_user_id = request.user.id
            obj.create_time = timezone.now()

        super().save_model(request, obj, form, change)


@admin.register(models.Question)
class Question(admin.ModelAdmin):
    """问题管理"""

    site_order = 2
    list_display = ('intent', 'status', 'answerType', 'answerMethod', 'answerTxt', 'create_time', 'update_time')
    fields = ('intent', 'status', 'answerType', 'answerMethod', 'answerTxt')


@admin.register(models.Answer)
class Answer(admin.ModelAdmin):
    """回答管理"""

    site_order = 2
    list_display = ('key', 'intentId', 'status', 'answerMethod', 'answerAudio', 'answerTxt', 'isDefault', 'create_time', 'update_time')
    fields = ('key', 'intentId', 'status', 'answerMethod', 'answerAudio', 'answerTxt', 'isDefault')


@admin.register(models.UserProfile)
class UserProfile(admin.ModelAdmin):
    """用户信息管理"""

    site_order = 2
    list_display = ('nickname', 'openId', 'status', 'avatar', 'sex', 'last_login')
    fields = ('nickname', 'openId', 'status', 'avatar', 'sex', 'last_login')


@admin.register(models.Record)
class Record(admin.ModelAdmin):
    site_order = 2
    list_display = ('userId', 'status', 'intent', 'tech', 'questionStr', 'answerStr', 'create_time')
    fields = ('userId', 'status', 'intent', 'tech', 'questionStr', 'answerStr')

@admin.register(models.Vicinity)
class Record(admin.ModelAdmin):
    site_order = 2
    list_display = ('projectName', 'vicinityData', 'status', 'create_time')
    fields = ('projectName', 'vicinityData', 'status')

