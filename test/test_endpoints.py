import unittest
from app import create_app
import os


class EndpointsTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_index_endpoint(self):
        resp = self.client.get('/api/v1/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json(), 'OK')


if __name__ == '__main__':
    unittest.main()
