import functools

from django.http import JsonResponse
from django.utils.translation import gettext as _

from .utils import PropertyJSONEncoder


def ajax_login_required(func):
    """Ajax接口登录限制装饰器（工厂函数）"""

    @functools.wraps(func)
    def new_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            res = {
                'code': 9900,
                'message': _('Unauthenticated'),
            }
            return JsonResponse(res, encoder=PropertyJSONEncoder, status=401)

    return new_func

# http://226cj31961.iok.la/static/audio/
