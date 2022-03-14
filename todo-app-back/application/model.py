import datetime
import jwt
from flask import Flask, current_app, Request
from flask_sqlalchemy import SQLAlchemy
from typing import Final, Union


DB: Final = SQLAlchemy()


def configure(app: Flask) -> None:
    DB.init_app(app)
    app.db = DB


class Task(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    name = DB.Column(DB.String(255), nullable=False)
    description = DB.Column(DB.String(255), nullable=True)
    date = DB.Column(DB.Date, nullable=False)
    done = DB.Column(DB.Boolean, default=False)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'))

    def __init__(self, task: dict) -> None:
        self.name = task.get('name')
        self.description = task.get('description')
        self.date = task.get('date')
        self.done = task.get('done')
        self.user_id = task.get('user_id')


class User(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    name = DB.Column(DB.String(255), nullable=False)
    email = DB.Column(DB.String(255), nullable=False, unique=True)
    password = DB.Column(DB.String(255), nullable=False)
    tasks = DB.relationship(Task, cascade='all, delete-orphan')

    def __init__(self, user: dict) -> None:
        self.id = user.get('id')
        self.name = user.get('name')
        self.email = user.get('email')
        self.password = user.get('password')

    def __str__(self) -> str:
        string = f'name: {self.name}, email: {self.email}'
        return string

    @staticmethod
    def encode_auth_token(user_id) -> Union[str, bytes]:
        try:
            payload: dict = {
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
    def decode_auth_token(auth_token: str) -> Union[int, str]:
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload: dict = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    @staticmethod
    def get_auth_token(request: Request) -> str:
        """
        Returns the auth token string from request headers
        """
        auth_header: str = request.headers.get('Authorization')
        auth_token: str = auth_header.split()[1] if auth_header else ''
        return auth_token

    @staticmethod
    def get_user_status(auth_token: str) -> Union['User', None]:
        """
        Return User object if query is completed successfully,
        or None if user don't exists
        """
        user: User = None
        if auth_token:
            resp: Union[int, str] = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
        return user
