# coding: u8

import datetime
from hashlib import md5 as m5
import traceback

now = datetime.datetime.now
now_str = lambda: dt2str(now())
yesterday = lambda: datetime.date.today() - datetime.timedelta(days=1)
yesterday_str = lambda: yesterday().strftime('%Y-%m-%d')
tomorrow = lambda: datetime.date.today() + datetime.timedelta(days=1)
tomorrow_str = lambda: tomorrow().strftime('%Y-%m-%d')
str2dt = lambda s: datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
dt2str = lambda dt: dt.strftime('%Y-%m-%d %H:%M:%S')
md5 = lambda s: m5(s).hexdigest()


def async(max_workers=10, debug=False):
    from concurrent.futures import ThreadPoolExecutor
    from functools import partial, wraps

    import tornado.ioloop
    import tornado.web

    EXECUTOR = ThreadPoolExecutor(max_workers=max_workers)

    def unblock(f):
        @tornado.web.asynchronous
        @wraps(f)
        def wrapper(*args, **kwargs):
            self = args[0]

            def callback(future):
                try:
                    self.write(future.result() or '')
                except:
                    if debug:
                        try:
                            self.write('<pre>%s</pre>' % traceback.format_exc())
                        except:
                            pass
                finally:
                    self.try_finish()

            EXECUTOR.submit(
                partial(f, *args, **kwargs)
            ).add_done_callback(
                lambda future: tornado.ioloop.IOLoop.instance().add_callback(
                    partial(callback, future)))

        return wrapper
    return unblock
