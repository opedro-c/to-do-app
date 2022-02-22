from flask import Flask
from model import configure as config_db
from serializer import configure as configure_ma
from flask_migrate import Migrate
from typing import Final


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///todo.db'
    config_db(app)
    configure_ma(app)
    from task import bp_tasks
    app.register_blueprint(bp_tasks)
    Migrate(app, app.db)
    return app


APP: Final = create_app()


@APP.route("/")
def home():
    return "Welcome to the To-Do App!"
