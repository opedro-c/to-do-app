import json
import unittest
from application.app import create_app
from application.model import Task, User
from application.serializer import TaskSchema
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
        ts = TaskSchema()
        task = ts.load(self.config['tasks'][1])
        task['user_id'] = 1
        self.app.db.session.add(Task(task))
        self.app.db.session.commit()

    def log_user_in(self):
        request_json = self.config['users'][0]
        return self.client.post('/auth/login', json=request_json)

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
        response = self.log_user_in()
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
        self.assertTrue(list(filter(lambda x: x['name'] == request_json['name'], response.json)))

    def test_update_task_info(self):
        token = self.log_user_in().json['auth_token']
        request_headers = {'Authorization': f'Bearer {token}'}
        response = self.client.get('/task', headers=request_headers)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json[0]['done'])
        response = self.client.put('/task/1', headers=request_headers, json={'done': True})
        self.assertEqual(response.status_code, 200, response.json)
        self.assertTrue(response.json['done'])
        response = self.client.get('/task', headers=request_headers)
        task_updated = list(filter(lambda x: x['id'] == 1, response.json))
        self.assertTrue(task_updated[0]['done'])

    def test_update_task_info_wrong_id(self):
        token = self.log_user_in().json['auth_token']
        request_headers = {'Authorization': f'Bearer {token}'}
        response = self.client.put('/task/5', headers=request_headers, json={'done': True})
        self.assertEqual(response.status_code, 400, response.json)

    def test_delete_tasks(self):
        token = self.log_user_in().json['auth_token']
        request_headers = {'Authorization': f'Bearer {token}'}
        response = self.client.get('/task', headers=request_headers)
        self.assertTrue(response.json)
        tasks_ids = [task['id'] for task in response.json]
        for id in tasks_ids:
            response = self.client.delete(f'/task/{id}', headers=request_headers)
            self.assertEqual(response.status_code, 200)
        response = self.client.get('/task', headers=request_headers)
        self.assertFalse(response.json)

    def test_delete_unexistent_task(self):
        token = self.log_user_in().json['auth_token']
        request_headers = {'Authorization': f'Bearer {token}'}
        response = self.client.delete('/task/5', headers=request_headers)
        self.assertEqual(response.status_code, 400, response.json)

    def test_create_task_with_unauthorized_user(self):
        request_json = self.config['tasks'][0]
        response = self.client.post('/task', json=request_json)
        self.assertEqual(response.status_code, 401, response.json)

    def test_update_and_delete_task_with_unauthorized_user(self):
        request_headers = {'Authorization': f'Bearer randomtokenhere'}
        response = self.client.put('/task/1', headers=request_headers, json={'done': True})
        self.assertEqual(response.status_code, 401, response.json)
        response = self.client.delete(f'/task/1', headers=request_headers)
        self.assertEqual(response.status_code, 401, response.json)

    def test_list_all_users(self):
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), len(self.config['users']))
        print(response.json)
        for i in range(len(self.config['users'])):
            self.assertEqual(self.config['users'][i]['name'], response.json[i]['name'])
            self.assertEqual(self.config['users'][i]['email'], response.json[i]['email'])
            self.assertFalse(response.json[i].get('password'))


if __name__ == '__main__':
    unittest.main()
