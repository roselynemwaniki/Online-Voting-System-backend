import unittest
from app import create_app, db
from models import User

class UserManagementTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_user(self):
        response = self.client.post('/api/register', json={
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'User registered successfully', response.data)

    def test_login_user(self):
        self.client.post('/api/register', json={
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'password123'
        })
        response = self.client.post('/api/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'token', response.data)

    def test_get_all_users(self):
        self.client.post('/api/register', json={
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'password123'
        })
        response = self.client.get('/api/users', headers={
            'Authorization': 'Bearer <admin_token>'  # Replace with a valid admin token
        })
        self.assertEqual(response.status_code, 200)

    def test_update_user(self):
        user = User(name='Test User', email='test@example.com', password='password123')
        db.session.add(user)
        db.session.commit()
        response = self.client.put(f'/api/user/{user.id}', json={
            'name': 'Updated User',
            'email': 'updated@example.com'
        }, headers={
            'Authorization': 'Bearer <admin_token>'  # Replace with a valid admin token
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        user = User(name='Test User', email='test@example.com', password='password123')
        db.session.add(user)
        db.session.commit()
        response = self.client.delete(f'/api/user/{user.id}', headers={
            'Authorization': 'Bearer <admin_token>'  # Replace with a valid admin token
        })
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
