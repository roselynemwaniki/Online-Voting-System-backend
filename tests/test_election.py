import unittest
from extensions import create_app, db  # Using relative import
from models import Election, User

class ElectionManagementTestCase(unittest.TestCase):
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

    def test_create_election(self):
        response = self.client.post('/api/elections', json={
            'title': 'Test Election',
            'description': 'A test election',
            'start_date': '2025-01-01',
            'end_date': '2025-01-10'
        }, headers={
            'Authorization': 'Bearer <admin_token>'  # Replace with a valid admin token
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Election created successfully', response.data)

    def test_get_all_elections(self):
        response = self.client.get('/api/elections')
        self.assertEqual(response.status_code, 200)

    def test_update_election(self):
        election = Election(title='Test Election', description='A test election', start_date='2025-01-01', end_date='2025-01-10')
        db.session.add(election)
        db.session.commit()
        response = self.client.put(f'/api/election/{election.id}', json={
            'title': 'Updated Election',
            'description': 'An updated test election'
        }, headers={
            'Authorization': 'Bearer <admin_token>'  # Replace with a valid admin token
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_election(self):
        election = Election(title='Test Election', description='A test election', start_date='2025-01-01', end_date='2025-01-10')
        db.session.add(election)
        db.session.commit()
        response = self.client.delete(f'/api/election/{election.id}', headers={
            'Authorization': 'Bearer <admin_token>'  # Replace with a valid admin token
        })
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
