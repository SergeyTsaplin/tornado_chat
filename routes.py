#-*- encoding: utf8 -*-
"""This module contains application routes
"""

from chat.handlers import ChatSocketHandler, ChatHistoryHandler
from base.handlers import MainHandler
from user.handlers import LoginHandler, SignupHandler, LogoutHandler


routes = [
    (r'/', MainHandler),
    (r'/chatsocket', ChatSocketHandler),
    (r'^/history$', ChatHistoryHandler),
    (r'^/login$', LoginHandler),
    (r'^/signup$', SignupHandler),
    (r'^/logout$', LogoutHandler),
]