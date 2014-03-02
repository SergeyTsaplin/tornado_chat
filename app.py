#-*- encoding: utf8 -*-
"""Module contains start tornado application logic. It's not recommended to
change it. All application settings locates in settings.py file in the same
directory
"""
import os.path

from tornado import ioloop, options, web
from mongoengine import connect

from routes import routes


options.define('port', default=8000, help="run application on specified port",
               type=int)
options.define('cookie_secret', default='secret', type=str)
options.define('db_name', default='mongo', help='database name',
               type=str)
options.define('db_host', default='localhost', help='specify database host')
options.define('db_port', default=27017, help='specify database port',
               type=int)
options.define('db_user', default=None, help='specify database user', type=str)
options.define('db_password', default=None,
               help='specify database user password', type=str)

options.define('debug', default=False, help="run application in debug mode",
               type=bool)


class Application(web.Application):
    def __init__(self):
        handlers = routes

        settings = dict(
            cookie_secret=options.options.cookie_secret,
            login_url="/login",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            debug=options.options.debug,
        )
        web.Application.__init__(self, handlers, **settings)


def main():
    try:
        options.parse_config_file('settings.py')
        options.parse_command_line()
    except AttributeError:
        options.options.print_help()
    app = Application()
    app.listen(options.options.port)
    io_loop = ioloop.IOLoop.instance()
    connect(options.options.db_name,
            host=options.options.db_host,
            port=options.options.db_port,
            username=options.options.db_user,
            password=options.options.db_password)
    io_loop.start()


if __name__ == "__main__":
    main()
