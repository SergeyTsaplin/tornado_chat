#-*- encoding: utf8 -*-
from hashlib import sha512

from mongoengine import Document, StringField, ReferenceField


class User(Document):
    """User model
    """

    username = StringField(max_length=255, required=True, unique=True)
    password = StringField(max_length=128, required=True)

    def to_dict(self):
        """Method converts current instance to dictionary. Returned dictionary
        doesn't contain password field for safety

        :rtype: dict
        """
        return {'id': self.pk.__str__(),
                'username': self.username}

    @classmethod
    def encrypt_password(cls, password):
        """Method encrypts password

        :param password: plain password
        :type password: str
        :return: encrypted password
        :rtype: str
        """
        return sha512(password).hexdigest()

    @classmethod
    def authenticate(cls, username, password):
        """Method authenticates user by its username and password

        :type username: str
        :param password: plain password
        :type password: str
        :return: user instance or None
        :rtype: :py:class:`user.models.User`
        """
        encrypted_password = cls.encrypt_password(password)
        return cls.objects(username=username, password=encrypted_password).\
            first()


class UserSession(Document):
    """User session model
    """
    user = ReferenceField(document_type=User)

    def to_dict(self):
        """Method converts current instance to dictionary.

        :rtype: dict
        """
        return {'id': self.pk.__str__(),
                'user': self.user}