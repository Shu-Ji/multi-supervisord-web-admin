#!/usr/bin/env python
# coding: u8

import env
env.setup()

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import options

import settings
from urls import url_patterns


class Application(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(
            self, url_patterns, **settings.TORNADO_SETTINGS)


def main():
    import g
    import cron

    app = Application()
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)

    logger = g.logger(__name__)
    logger.info('tornado servering on: http://%s:%d' % (
        options.host, options.port))
    http_server.listen(options.port)

    cron.start_master()

    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
