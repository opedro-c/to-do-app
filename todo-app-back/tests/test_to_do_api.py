from asyncio import tasks
from distutils.command.config import config
import json
import unittest
from application.app import create_app
from application.model import User
from werkzeug.security import generate_password_hash


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test_todo.db'
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.app.db.create_all()
        self.config = json.load(open('tests/config.json'))
        self.client = self.app.test_client()
        self.populate_db()

    def tearDown(self):
        self.app.db.drop_all()

    def populate_db(self):
        for user in self.config['users']:
            user_copy = user.copy()
            user_copy['password'] = generate_password_hash(user['password'])
            self.app.db.session.add(User(user_copy))
        self.app.db.session.commit()

    def test_server_running(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_register_user(self):
        request_json = self.config['user_register_json']
        response = self.client.post('/auth/register', json=request_json)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json.get('auth_token'))
        self.assertFalse(response.json.get('id'))

    def test_existent_register_user(self):
        request_json = self.config['users'][1]
        response = self.client.post('/auth/register', json=request_json)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json.get('auth_token'))
        self.assertFalse(response.json.get('id'))

    def test_login_user(self):
        request_json = self.config['users'][0]
        response = self.client.post('/auth/login', json=request_json)
        self.assertEqual(response.status_code, 200, response.json)
        self.assertTrue(response.json.get('auth_token'))
        self.assertFalse(response.json.get('id'))

    def test_login_another_user(self):
        request_json = self.config['users'][1]
        response = self.client.post('/auth/login', json=request_json)
        self.assertEqual(response.status_code, 200, response.json)
        self.assertTrue(response.json.get('auth_token'))
        self.assertFalse(response.json.get('id'))

    def test_wrong_login(self):
        request_json = self.config['wrong_user']
        response = self.client.post('/auth/login', json=request_json)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json.get('auth_token'))

    def test_create_task_and_retrieve_later(self):
        user_credentials = self.config['users'][1]
        token = self.client.post('/auth/login', json=user_credentials).json['auth_token']
        request_headers = {'Authorization': f'Bearer {token}'}
        request_json = self.config['tasks'][0]
        response = self.client.post('/task', json=request_json, headers=request_headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json.get('name'), request_json['name'])
        response = self.client.get('/task', headers=request_headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any([request_json['name'] == task['name'] for task in self.config['tasks']]))


if __name__ == '__main__':
    unittest.main()
