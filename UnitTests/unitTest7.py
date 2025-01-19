import unittest
from AppAvtoDetali import RegisterScreen

class TestRegisterScreen(unittest.TestCase):
    def setUp(self):
        self.app = RegisterScreen()
    def test_check_phone_num_False(self):
        self.assertEqual(self.app.check_phone_num("1234"), False)
    def test_check_phone_num_True(self):
        self.assertEqual(self.app.check_phone_num("12345678901"), True)
    def test_is_phone_unique_False(self):
        self.assertEqual(self.app.is_phone_unique("12345678901"), False)
    def test_is_phone_unique_True(self):
        self.assertEqual(self.app.is_phone_unique("12345678909"), True)