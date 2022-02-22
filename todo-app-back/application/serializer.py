from typing import Final
from flask_marshmallow import Marshmallow
from model import Task

MA: Final = Marshmallow()


def configure(app):
    MA.init_app(app)


class TaskSchema(MA.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
