import datetime
import jwt

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from typing import Final


DB: Final = SQLAlchemy()


def configure(app):
    DB.init_app(app)
    app.db = DB


class Task(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    name = DB.Column(DB.String(255), nullable=False)
    description = DB.Column(DB.String(255), nullable=True)
    date = DB.Column(DB.Date, nullable=False)
    done = DB.Column(DB.Boolean, default=False)

    def __init__(self, task: dict):
        self.name = task.get('name')
        self.description = task.get('description')
        self.date = task.get('date')
        self.done = task.get('done')


class User(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    name = DB.Column(DB.String(255), nullable=False)
    email = DB.Column(DB.String(255), nullable=False, unique=True)
    password = DB.Column(DB.String(255), nullable=False)

    def __init__(self, user: dict):
        self.id = user.get('id')
        self.name = user.get('name')
        self.email = user.get('email')
        self.password = user.get('password')

    @staticmethod
    def encode_auth_token(user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=1),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY')
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

