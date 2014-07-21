# coding: u8

import tornado.web

from handlers.index import *


__all__ = ['url_patterns']


# exchange name and kwargs
url = lambda u, h, n=None, k=None: tornado.web.URLSpec(u, h, k, n)

url_patterns = [
    url(r'/', IndexHandler, 'index'),
    url(r'/reset/password', ResetPasswordHandler, 'reset-password'),
    url(r'/process/add', IndexHandler, 'add-process'),
    url(r'/host/detail', HostDetailHandler, 'host-detail'),

    url(r'.*', NotfoundHandler, '404'),
]
