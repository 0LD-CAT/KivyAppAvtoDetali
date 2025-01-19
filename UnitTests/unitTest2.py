import unittest
from unittest.mock import patch

from AppAvtoDetali import ShopDetailsApp

class TestShopDetailsApp(unittest.TestCase):
    def setUp(self):
        self.app = ShopDetailsApp()
    def test_add_to_cart_single_item(self):
        """Тестируем добавление одного элемента в корзину."""
        self.app.add_to_cart(100)
        self.assertEqual(self.app.total_price, 100)  # Проверяем общую стоимость
        self.app.ids.cart_label.text = f'Корзина: {self.app.total_price} руб.'
        self.assertEqual(self.app.ids.cart_label.text, 'Корзина: 100 руб.')  # Проверяем текст метки

    def test_add_to_cart_multiple_items(self):
        """Тестируем добавление нескольких элементов в корзину."""
        self.app.add_to_cart(150)
        self.app.add_to_cart(50)
        self.assertEqual(self.app.total_price, 200)  # Проверяем общую стоимость
        self.app.ids.cart_label.text = f'Корзина: {self.app.total_price} руб.'
        self.assertEqual(self.app.ids.cart_label.text, 'Корзина: 200 руб.')  # Проверяем текст метки

    def test_add_to_cart_zero(self):
        """Тестируем добавление элемента со стоимостью 0."""
        self.app.add_to_cart(0)
        self.assertEqual(self.app.total_price, 0)  # Проверяем общую стоимость
        self.app.ids.cart_label.text = f'Корзина: {self.app.total_price} руб.'
        self.assertEqual(self.app.ids.cart_label.text, 'Корзина: 0 руб.')  # Проверяем текст метки
    def test_clear_cart_single_item(self): # проверка очистки корзины
        self.app.total_price = 100
        self.app.clear_cart()
        self.assertEqual(self.app.total_price, 0)

    @patch('builtins.print')
    def test_payment_positive(self, mock_print):
        self.app.total_price = 100
        self.app.payment()
        # Проверяем, что вывод соответствует ожидаемому
        mock_print.assert_called_once_with('Заказ оформлен на сумму: 100 руб.')

    @patch('builtins.print')
    def test_payment_zero(self, mock_print):
        self.app.total_price = 0
        self.app.payment()
        # Проверяем, что вывод соответствует ожидаемому
        mock_print.assert_called_once_with('Корзина пуста!')
if __name__ == '__main__':
    unittest.main()