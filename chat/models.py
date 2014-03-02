#-*- encoding: utf8 -*-
from datetime import datetime

from mongoengine import Document, StringField, DateTimeField, ReferenceField

from user.models import User


class Message(Document):
    """Chat message model
    """

    text = StringField(max_length=1024, required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    user = ReferenceField(document_type=User)

    @classmethod
    def get_history_query(cls, first_message_id=None):
        """Method returns mongoengine queryset by parameters

        :param first_message_id: id of first message client already have
        :type first_message_id: str
        :return: mongoengine queryset
        :rtype: :py:class:`mongoengine.queryset.queryset.QuerySet`
        """
        if not first_message_id:
            return Message.objects.order_by('-created_at')

        first_message = Message.objects.get(pk=first_message_id)
        return Message.objects(created_at__lt=first_message.created_at).\
            order_by('-created_at')

    def to_dict(self):
        """Method converts current instance to dictionary

        :rtype: dict
        """
        return {'id': self.pk.__str__(),
                'text': self.text,
                'created_at':
                    self.created_at.__format__("%Y/%m/%d %H:%M:%S UTC"),
                'user': self.user.to_dict()}