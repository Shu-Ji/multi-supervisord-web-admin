# coding: u8

import os
from tornado.options import define, options

path = lambda root, *a: os.path.join(root, *a)
ROOT = os.path.dirname(os.path.abspath(__file__))

try:
    define("host", default='0.0.0.0', help="run on the given host", type=str)
    define("port", default=8090, help="run on the given port", type=int)
    define("debug", default=True, help="debug mode", type=bool)
    import tornado
    tornado.options.parse_command_line()
except:
    options.debug = True

DEBUG = options.debug

MEDIA_ROOT = path(ROOT, 'media')
STATIC_ROOT = path(ROOT, 'static')
TEMPLATE_ROOT = path(ROOT, 'templates')
DB_PATH = path(ROOT, 'dev.db')


TORNADO_SETTINGS = {
    'autoescape': True,
    'cookie_secret': '^X@s6Gwf#BM]hello54sWf@@kitty!fNd:f=>:)$',
    'debug': DEBUG,
    'static_path': STATIC_ROOT,
    'session_id_cookie_name':'mswa_SESSION_ID',
}
MAX_ASYNC_TASKS_POOL_SIZE = 100
