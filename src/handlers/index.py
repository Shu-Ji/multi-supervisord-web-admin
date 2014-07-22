# coding: u8

import tornado.web

from g import async
from handlers.base import BaseHandler
from models import User as U, Host as H
import supervisord as sv


class NotfoundHandler(BaseHandler):
    def get(self):
        raise tornado.web.HTTPError(404)


class HostDetailHandler(BaseHandler):
    @async
    def get(self):
        host, port = self.input('host'), self.input('port')
        handler = self.fake
        host = H.get_one_host_info(handler, host, port)
        handler.db.close()
        self.write_json(err=False, info=sv.get_one_host_info(host))


class IndexHandler(BaseHandler):
    def get(self, pid=None):
        path = self.request.path
        if path == self.reverse_url('index'):
            self.render('index.html', hosts=H.get_all_active_hosts(self))
        elif pid is not None:
            host = H.get_one_host_info_by_id(self.db, pid)
            if host is None:
                return self.redirect('/404')
            self.render('add-process.html', stype='update', host=host)
        elif path == self.reverse_url('add-process'):
            self.render('add-process.html', stype='add')

    def post(self):
        t = 'post_' + self.input('action')
        if hasattr(self, t):
            getattr(self, t)()

    def post_update(self):
        user = self.input('user')
        pwd = self.input('pwd')
        host = self.input('host')
        port = self.input('port')
        id = self.input('id')

        ret = {'err': not H.update(self.db, id, user, pwd, host, port)}
        if ret['err']:
            ret['msg'] = u'更新失败。不存在的配置。错误码：%s' % id

        self.write(ret)

    def post_del(self):
        id = self.input('id')

        ret = {'err': not H.delete(self.db, id)}
        if ret['err']:
            ret['msg'] = u'删除失败。不存在的配置。错误码：%s' % id

        self.write(ret)

    def post_add(self):
        user = self.input('user')
        pwd = self.input('pwd')
        host = self.input('host')
        port = self.input('port')

        ret = {'err': not H.add(self, user, pwd, host, port)}
        if ret['err']:
            ret['msg'] = u'添加失败。已存在相同的配置：%s:%s' % (host, port)

        self.write(ret)

    @async
    def post_stop(self):
        host = self.input('host')
        port = self.input('port')
        name = self.input('name')
        group = self.input('group')

        handler = self.fake
        host = H.get_one_host_info(handler, host, port)
        sv.stop_one_process(host, name, group)
        handler.db.close()

    @async
    def post_restart(self):
        host = self.input('host')
        port = self.input('port')
        name = self.input('name')
        group = self.input('group')

        handler = self.fake
        host = H.get_one_host_info(handler, host, port)
        sv.restart_one_process(host, name, group)
        handler.db.close()


class ResetPasswordHandler(BaseHandler):
    def get(self):
        self.render('reset-password.html')

    def post(self):
        old = self.input('old')
        new = self.input('new')
        confirm = self.input('confirm')

        if new != confirm:
            return self.write_json(err=True, msg=u'两次输入的密码不一致。')

        ret = {}
        ret['err'] = not U.reset_password(self, old, new)
        if ret['err']:
            ret['msg'] = u'原始密码不正确。'

        self.write(ret)
