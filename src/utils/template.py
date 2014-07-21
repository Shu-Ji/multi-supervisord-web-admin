# coding: u8

import jinja2


class UndefinedSilently(jinja2.Undefined):
    __unicode__ = __str__ = lambda *args, **kwargs: u''
    __call__ = __getattr__ = lambda *args, **kwargs: UndefinedSilently()


class Render(object):
    def __init__(self, template_path, **kw):
        from jinja2 import Environment, FileSystemLoader

        extra = kw.pop('extra', [])
        self._env = Environment(loader=FileSystemLoader(template_path), **kw)
        self._env.globals.update(extra)

    def add_filters(self, filters):
        """Add extra filters into jinja2 environment.

        filters: dict-like object
        """
        self._env.filters.update(filters)

    def render(__this, handler, path, *args, **kw):
        # use __this to make `self` availible in kw, usefull in **locals()
        # make tornado buildin template variables available in jinja2
        kw = dict(*args, **kw)
        kw.pop('self', None)
        args = dict(
            handler=handler,
            request=handler.request,
            #locale=handler.locale,
            #_=handler.locale.translate,
            static_url=handler.static_url,
            xsrf=handler.xsrf_form_html,
            reverse_url=handler.application.reverse_url
        )
        try:
            args['session'] = handler.session
        except AttributeError:
            pass

        kw.update(args)

        flush = kw.pop('flush', True)
        html = __this._env.get_template(path).render(**kw)

        if not flush:
            # only return rendered html
            return html
        else:
            # flush to client browser with tornado write method
            handler.write(html)

    def macro(self, path):
        return self._env.get_template(path).module
