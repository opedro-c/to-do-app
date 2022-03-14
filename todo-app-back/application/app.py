from flask import Flask
from model import configure as config_db
from serializer import configure as configure_ma
from flask_migrate import Migrate
from secrets import token_hex


def create_app() -> Flask:
    app: Flask = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///todo.db'
    app.config['SECRET_KEY'] = token_hex(16)
    config_db(app)
    configure_ma(app)

    from task import bp_tasks
    app.register_blueprint(bp_tasks)
    from user import bp_user
    app.register_blueprint(bp_user)

    Migrate(app, app.db)
    return app
