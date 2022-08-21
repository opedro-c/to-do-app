from flask import Blueprint, current_app, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from model import User
from serializer import UserSchema


bp_user = Blueprint('user', __name__)


@bp_user.route('/auth/register', methods=['POST'])
def register():
    us = UserSchema()
    user = us.load(request.json)
    user_found = User.query.filter_by(email=user.get('email')).first()
    if user_found:
        return jsonify({
            'status': 'fail',
            'message': 'User already exists. Please log in.'
            }), 400
    else:
        # Register user
        user['password'] = generate_password_hash(user['password'])
        current_app.db.session.add(User(user))
        current_app.db.session.commit()
        # Generate auth token
        user_registered = User.query.filter(User.email == user['email']).first()
        auth_token = User.encode_auth_token(user_registered.id)
        response = {
            'status': 'success',
            'message': 'Successfully registered',
            'auth_token': auth_token.decode()
        }
        return jsonify(response), 201


@bp_user.route('/auth/login', methods=['POST'])
def login():
    login_request = request.json
    user = User.query.filter_by(email=login_request.get('email')).first()
    if user and check_password_hash(user.password, login_request.get('password')):
        auth_token = User.encode_auth_token(user.id)
        if auth_token:
            response = {
                'status': 'success',
                'message': 'Successfully logged in',
                'auth_token': auth_token.decode()
            }
            return jsonify(response), 200
    response = {'status': 'fail', 'message': 'Login failed, please try again'}
    return jsonify(response), 400


@bp_user.route('/auth/status', methods=['GET'])
def status():
    user = User.get_user_status(request)
    if user:
        response = {
            'status': 'success',
            'data': {
                'id': user.id,
                'name': user.name
            }
        }
        return jsonify(response), 200
    response = {'status': 'fail', 'message': 'Provide a valid auth token.'}
    return jsonify(response), 401


@bp_user.route('/users', methods=['GET'])
def get_all_users():
    us = UserSchema(many=True)
    query = current_app.db.session.query(User.name, User.email).all()
    return us.jsonify(query), 200
