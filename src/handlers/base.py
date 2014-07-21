# coding: u8

import tornado.web
from tornado.util import ObjectDict

import g
import models
import settings

import utils


class BaseHandler(tornado.web.RequestHandler):
    """A class to collect common handler methods - all other handlers should
    subclass this one.
    """

    @property
    def reverse_url(self):
        return self.application.reverse_url

    def try_finish(self):
        try:
            self.finish()
        except:
            pass

    def on_finish(self):
        self.close_db()

    def close_db(self):
        """self.db is request handler singled, self.dbm is used in models"""
        try:
            self.db.commit()
        except:
            import traceback
            self.loge(traceback.format_exc())
            self.db.rollback()
        try:
            self.db.close()
        except:
            import traceback
            self.loge(traceback.format_exc())

    def http_basic_auth(self):
        def auth():
            self.set_status(401)
            self.set_header('WWW-Authenticate', 'Basic realm=Restricted')
            self._transorms = []
            self.finish()
            return False

        auth_header = self.request.headers.get('Authorization')
        if auth_header is None or not auth_header.startswith('Basic '):
            return auth()

        import base64
        auth_decoded = base64.decodestring(auth_header[6:])
        username, password = auth_decoded.split(':', 2)

        user = self.db.query(models.User).filter_by(name=username).first()
        valid = bool(user) and (utils.md5(password) == user.pwd)

        if not valid:
            return auth()

        self.username = username
        return True

    @property
    def fake(self):
        return ObjectDict(db=models.db_factory())

    def prepare(self):
        self.db = models.db_factory()

        if not self.http_basic_auth():
            return

    @property
    def session_id(self):
        return self.get_secure_cookie(settings.SESSION_ID_NAME)

    def get_current_user(self):
        user = self.session.get('user')
        return user and ObjectDict(user)

    @property
    def logger(self):
        return g.logger(__name__)

    @property
    def logi(self):
        return self.logger.info

    @property
    def loge(self):
        return self.logger.error

    @property
    def logd(self):
        return self.logger.debug

    @property
    def logw(self):
        return self.logger.warn

    def render(___, path, *args, **kwargs):
        kw = dict(*args, **kwargs)
        kw.pop('self', None)
        g.render.render(___, path, **kw)

    def render_html(self, path, **kwargs):
        kwargs['flush'] = False
        return g.render.render(self, path, **kwargs)

    def macro(self, path):
        return g.render.macro(path)

    def input(self, name, default=None, strip=True):
        return super(BaseHandler, self).get_argument(name, default, strip)

    def write_json(self, *args, **kwargs):
        self.write(dict(*args, **kwargs))
