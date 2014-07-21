# coding: u8

import datetime
import json

from jinja2 import evalcontextfilter


@evalcontextfilter
def _unicode(eval_ctx, value, encoding='u8'):
    if value is None:
        return
    try:
        return value.decode(encoding)
    except UnicodeEncodeError:
        return value


@evalcontextfilter
def date(eval_ctx, value):
    if isinstance(value, str) or isinstance(value, unicode):
        value = datetime.datetime.strptime(value, '%Y-%m-%d')
    return '' if not value else value.date()


@evalcontextfilter
def dt(eval_ctx, value):
    return '' if not value else value.strftime('%Y-%m-%d %H:%M:%S')


@evalcontextfilter
def int2dt(eval_ctx, value, fmt='%m-%d %H:%M:%S'):
    """integer to datetime format"""
    return datetime.datetime.fromtimestamp(value).strftime(fmt)


@evalcontextfilter
def json_dumps(eval_ctx, value):
    return json.dumps(value)


filters = {
    'date': date,
    'unicode': _unicode,
    'json_dumps': json_dumps,
    'int2dt': int2dt,
    'dt': dt,
}
