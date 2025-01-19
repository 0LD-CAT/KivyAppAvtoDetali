import unittest
from unittest.mock import MagicMock, patch

from AppAvtoDetali import LoginScreen

class TestLoginScreen(unittest.TestCase):
    def setUp(self):
        self.app = LoginScreen()
        # Имитация объектов для ids
        self.app.ids = {
            'phone_input': MagicMock(),
            'password_input': MagicMock()
        }
        self.app.show_error = MagicMock()
        self.app.open_main_app = MagicMock()

    def test_read_login_csv(self): # Проверка на чтение данных
        check_data = [['89519308616','123'],
                      ['89519308515','123'],
                      ['12345678901','123'],
                      ['11111111111','111']]
        # Вызов метода для чтения данных из CSV
        test_data = self.app.read_login_csv()
        # Проверяем, что данные были загружены корректно
        self.assertEqual(test_data, check_data)
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='Phone,Password\n1234567890,password123\n')
    def test_login_success(self, mock_file): # Проверка на успешный вход
        # Настройка ввода телефона и пароля
        self.app.ids['phone_input'].text = '1234567890'
        self.app.ids['password_input'].text = 'password123'

        # Вызов метода логина
        self.app.login()

        # Проверяем, что основной экран открыт и поля очищены
        self.app.open_main_app.assert_called_once()
        self.assertEqual(self.app.ids['phone_input'].text, "")
        self.assertEqual(self.app.ids['password_input'].text, "")

    def test_login_empty_fields(self): # Проверка на пустой ввод
        # Пустые поля ввода
        self.app.ids['phone_input'].text = ''
        self.app.ids['password_input'].text = ''

        # Вызов метода логина
        self.app.login()

        # Проверяем, что отображается ошибка
        self.app.show_error.assert_called_once_with("Пожалуйста, заполните все поля.")

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_login_file_not_found(self, mock_file): # Проверка на ошибку при чтении или открытии файла данных
        # Настройка ввода телефона и пароля
        self.app.ids['phone_input'].text = '1234567890'
        self.app.ids['password_input'].text = 'password123'

        # Вызов метода логина
        self.app.login()

        # Проверяем, что отображается ошибка при чтении данных
        self.app.show_error.assert_called_once_with("Ошибка при чтении данных.")

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='Phone,Password\n1234567890,password123\n')
    def test_login_invalid(self, mock_file): # проверка на неправильность телефена или пароля
        # Настройка ввода телефона и пароля
        self.app.ids['phone_input'].text = 'wrong_phone'
        self.app.ids['password_input'].text = 'wrong_password'

        # Вызов метода логина
        self.app.login()

        # Проверяем, что отображается ошибка для неверных учетных данных
        self.app.show_error.assert_called_once_with("Неверный номер телефона или пароль.")
        self.assertEqual(self.app.ids['password_input'].text, "")
if __name__ == '__main__':
    unittest.main()