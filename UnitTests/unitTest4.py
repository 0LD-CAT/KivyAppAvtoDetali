import unittest
from unittest.mock import mock_open, patch, MagicMock

from AppAvtoDetali import RegisterScreen

class TestRegisterScreen(unittest.TestCase):
    def setUp(self):
        self.app = RegisterScreen()
        self.app.ids = {
            'phone_input': MagicMock(),
            'password_input': MagicMock()
        }
        self.app.show_error = MagicMock()
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_register_success(self, mock_open):  # Проверка на успешную рег-ию
        # Настраиваем ввод
        self.app.ids['phone_input'].text = '12345678901'
        self.app.ids['password_input'].text = 'password123'
        self.app.is_phone_unique = MagicMock(return_value=True) # проверка на уникальность телефона
        self.app.write_log_csv = MagicMock(return_value=True) # проверка на успешную запись данных

        # Запускаем регистрацию
        self.app.register()

        # Проверяем, что поля ввода очищены
        self.assertEqual(self.app.ids['phone_input'].text, "")
        self.assertEqual(self.app.ids['password_input'].text, "")

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_register_empty_fields(self, mock_open): # Проверка на пустой ввод
        self.app.ids['phone_input'].text = ''
        self.app.ids['password_input'].text = ''

        with patch.object(self.app, 'show_error') as mock_show_error:
            self.app.register()
            mock_show_error.assert_called_once_with("Пожалуйста, заполните все поля.")

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_register_invalid_phone_length(self, mock_open): # Проверка на длинну пароля
        self.app.ids['phone_input'].text = '12345'
        self.app.ids['password_input'].text = 'password123'

        with patch.object(self.app, 'show_error') as mock_show_error:
            self.app.register()
            mock_show_error.assert_called_once_with("Номер телефона должен состоять из 11 цифр!")

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_register_invalid_phone_characters(self, mock_open): # Проверка на содержание пароля
        self.app.ids['phone_input'].text = '12345фывыфвфывфыв'
        self.app.ids['password_input'].text = 'password123'

        with patch.object(self.app, 'show_error') as mock_show_error:
            self.app.register()
            mock_show_error.assert_called_once_with("Номер телефона должен состоять из 11 цифр!")
if __name__ == '__main__':
    unittest.main()