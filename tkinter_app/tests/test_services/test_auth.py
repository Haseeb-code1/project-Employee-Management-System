import unittest
from unittest.mock import patch
from app.services.auth import login

class TestAuthService(unittest.TestCase):
    @patch('app.services.auth.fetch_one')
    def test_login_success(self, mock_fetch_one):
        mock_fetch_one.return_value = {"id": 1, "username": "admin", "role": "Admin"}
        user = login("admin", "admin123")
        self.assertIsNotNone(user)
        self.assertEqual(user['username'], "admin")

    @patch('app.services.auth.fetch_one')
    def test_login_failure(self, mock_fetch_one):
        mock_fetch_one.return_value = None
        user = login("admin", "wrongpass")
        self.assertIsNone(user)

if __name__ == '__main__':
    unittest.main()
