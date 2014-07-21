# coding: u8

import logging

import filters
import settings
from utils import template, async


__all__ = ['logger', 'render']


def logger(name):
    l = logging.getLogger('mswa.' + name)
    l.setLevel(logging.INFO if settings.DEBUG else logging.ERROR)
    return l

async = async(settings.MAX_ASYNC_TASKS_POOL_SIZE, settings.DEBUG)

# add python builtins functions to jinja2 template
_extra = {
    'settings': settings,
}
_extra.update(__builtins__)

render = template.Render(
    auto_reload=True,
    #cache_size=0,
    autoescape=False,
    extensions=['jinja2.ext.do', 'jinja2.ext.loopcontrols'],
    extra=_extra,
    line_comment_prefix='@#',
    line_statement_prefix='@',
    template_path=settings.TEMPLATE_ROOT,
    trim_blocks=True,
    undefined=template.UndefinedSilently,
)
render.add_filters(filters.filters)
