from typing import Any, Callable, Union, Tuple
from flask import (
    Blueprint, current_app, request,
    jsonify, Response, Request
    )
from model import Task, User
from serializer import TaskSchema

bp_tasks = Blueprint('tasks', __name__)


def get_request_user(request_received: Request):
    return User.get_user_status(User.get_auth_token(request_received))


def login_required(func: Callable) -> Callable:
    def check_auth() -> Union[Any, Tuple[Response, int]]:
        user: Union[User, None] = get_request_user(request)
        if user:
            return func()
        else:
            return jsonify(False), 401
    check_auth.__name__ = func.__name__
    return check_auth


@bp_tasks.route('/')
def hello():
    return 'Hello World'


@bp_tasks.route('/task', methods=['GET'])
@login_required
def get():
    ts = TaskSchema(many=True)
    user = get_request_user(request)
    query = Task.query.filter(Task.user_id == user.id)
    return ts.jsonify(query), 200


@bp_tasks.route('/task', methods=['POST'])
@login_required
def create():
    ts = TaskSchema()
    user = get_request_user(request)
    task = ts.load(request.json)
    task['user_id'] = user.id
    current_app.db.session.add(Task(task))
    current_app.db.session.commit()
    return ts.jsonify(task), 201


@bp_tasks.route('/task/<task_id>', methods=['DELETE'])
def delete(task_id):
    user = get_request_user(request)
    query = Task.query.filter(Task.id == task_id)
    if not user: return jsonify(False), 401
    if not query.first():
        response = {
            'status': 'fail',
            'message': 'Task not found'
        }
        return jsonify(response), 400
    Task.query.filter(Task.id == task_id).delete()
    current_app.db.session.commit()
    return jsonify(True), 200


@bp_tasks.route('/task/<task_id>', methods=['PUT'])
def update(task_id):
    user = get_request_user(request)
    if not user: return jsonify(False), 401
    ts = TaskSchema()
    query = Task.query.filter(Task.id == task_id)
    if not query.first():
        response = {
            'status': 'fail',
            'message': 'Task not found'
        }
        return jsonify(response), 400
    query.update(request.json)
    current_app.db.session.commit()
    return ts.jsonify(query.first())
