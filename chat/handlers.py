#-*- encoding: utf8 -*-
import logging

from tornado import escape, websocket, web
from mongoengine.errors import DoesNotExist, ValidationError

from .models import Message
from base.handlers import BaseHandler


class ChatSocketHandler(BaseHandler, websocket.WebSocketHandler):
    """Chat web socket handler. Provides chat messaging
    """
    waiters = set()

    def allow_draft76(self):
        # for iOS 5.0 Safari
        return True

    @web.authenticated
    def open(self):
        ChatSocketHandler.waiters.add(self)

    def on_close(self):
        ChatSocketHandler.waiters.remove(self)

    @classmethod
    def send_updates(cls, chat_message):
        logging.debug("sending message to %d waiters", len(cls.waiters))
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat_message)
            except:
                logging.error("Error sending message", exc_info=True)

    def _store_message(self, chat_message):
        new_message = Message(**chat_message)
        return new_message.save()

    @web.authenticated
    def on_message(self, message):
        logging.debug("got message %r", message)
        try:
            parsed = escape.json_decode(message)
            chat_message = {
                "user": self.get_current_user(),
                "text": parsed["text"],
            }
            chat_message = self._store_message(chat_message).to_dict()
            ChatSocketHandler.send_updates(chat_message)
        except (KeyError, ValueError):
            logging.error("Invalid message %s", message)


class ChatHistoryHandler(BaseHandler):
    """Chat history handler. Provides getting of old messages
    """

    def get(self):
        self.set_header("Content-Type", "application/json")

        first_message_id = self.get_argument('first_message_id', default=None)
        try:
            count = int(self.get_argument('count', default=10))
        except ValueError:
            count = 10

        try:
            messages = Message.get_history_query(first_message_id)[:count]
        except DoesNotExist:
            self.write(escape.json_encode({'error': 'Message not found'}))
            return
        except ValidationError:
            self.write(escape.json_encode({'error': 'Invalid message id'}))
            return

        response = escape.json_encode(
            [m.to_dict() for m in reversed(messages)])
        self.write(response)
