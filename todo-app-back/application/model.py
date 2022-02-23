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
        self.id = task.get('id')
        self.name = task.get('name')
        self.description = task.get('description')
        self.date = task.get('date')
        self.done = task.get('done')
