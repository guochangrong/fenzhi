from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PropertyConfig(AppConfig):
    '''应用配置'''

    name = 'property'
    verbose_name = _('property')