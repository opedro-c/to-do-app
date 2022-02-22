from flask import Blueprint, current_app, request
from model import Task
from serializer import TaskSchema

bp_tasks = Blueprint('tasks', __name__)


@bp_tasks.route('/show', methods=['GET'])
def show():
    ts = TaskSchema(many=True)
    result = Task.query.all()
    return ts.jsonify(result), 200


@bp_tasks.route('/create', methods=['POST'])
def create():
    ts = TaskSchema()
    task = ts.load(request.json)
    current_app.db.session.add(Task(task))
    current_app.db.session.commit()
    return ts.jsonify(task), 201
