#-*- encoding: utf8 -*-
from tornado import web
from mongoengine.errors import DoesNotExist

from user.models import UserSession


class BaseHandler(web.RequestHandler):
    """Base application handler. Overrides get_current_user method. All hadlers
    working with users have to inherit from it
    """

    def get_current_user(self):
        session = self.get_secure_cookie('session')
        if not session:
            return None

        try:
            session = UserSession.objects.get(pk=session)
        except DoesNotExist:
            return None

        return session.user


class MainHandler(BaseHandler):
    """Main application controller. Provides main page working
    """

    @web.authenticated
    def get(self):
        self.render('index.html', user=self.current_user)