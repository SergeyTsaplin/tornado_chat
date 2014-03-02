#-*- encoding: utf8 -*-
from __future__ import absolute_import

from tornado import web
from mongoengine.errors import NotUniqueError

from .models import UserSession, User
from base.handlers import BaseHandler


class LoginMixin(object):
    """Handler mixin. Provides user login
    """

    def _login(self, user):
        session = UserSession(user=user)
        session.save()
        self.set_secure_cookie('session', session.pk.__str__())
        self.redirect('/')


class LoginHandler(BaseHandler, LoginMixin):
    """Handler provides UI for login page
    """

    def get(self):
        self.render('login.html', failed=False, username=None)

    def post(self):
        username = self.get_argument('username').strip()
        password = self.get_argument('password').strip()
        message = None
        user = None
        if not password or not username:
            message = u'Username and password required'
        else:
            user = User.authenticate(username, password)

        if user:
            self._login(user)
        elif not message:
            message = u'Invalid username or password'

        self.render('login.html', username=username, failed=True,
                    message=message)


class SignupHandler(BaseHandler, LoginMixin):
    """Handler provides UI for signup page
    """

    def get(self):
        self.render('signup.html', failed=False)

    def post(self):
        username = self.get_argument('username').strip()
        password = self.get_argument('password').strip()
        confirmation = self.get_argument('confirmation')
        message = None
        if password != confirmation:
            message = u'Password and confirmation doesn\'t match'
        if not password or not username:
            message = u'All fields required'
        encrypted_password = User.encrypt_password(password)
        if not message:
            user = User(username=username,
                        password=encrypted_password)
            try:
                user.save()
                self._login(user)
                return
            except NotUniqueError:
                message = u'Username "{0}" already exists'.format(username)

        self.render('signup.html', failed=True, message=message)


class LogoutHandler(BaseHandler):
    """Handler provides users logout
    """

    @web.authenticated
    def post(self):
        session = self.get_secure_cookie('session')
        if session and session != 'None':
            UserSession.objects(pk=session).delete()
        self.clear_cookie('session')
        self.redirect('/login')