import unittest
from AppAvtoDetali import LoginScreen
from unittest.mock import mock_open, patch
class TestLoginScreen(unittest.TestCase):
    def setUp(self):
        self.app = LoginScreen()
    def test_check_phone_pass_False(self):
        self.assertEqual(self.app.check_phone_pass('8488888', 'retert'), False)
    def test_check_phone_pass_True(self):
        self.assertEqual(self.app.check_phone_pass('12345678901', '123'), True)
    @patch('builtins.open', new_callable=mock_open)
    def test_check_phone_pass_None(self, mock_file):
        mock_file.side_effect = FileNotFoundError
        self.assertEqual(self.app.check_phone_pass('12345678901', '123'), None)
    @patch.object(LoginScreen, 'read_login_csv', return_value=None)
    def test_check_phone_pass_None(self, mock_read_login_csv):
        self.assertEqual(self.app.check_phone_pass('12345678901', '123'), None)