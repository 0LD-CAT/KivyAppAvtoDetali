import unittest
from AppAvtoDetali import ShopDetailsApp

class TestShopDetailsApp(unittest.TestCase):
    def setUp(self):
        self.app = ShopDetailsApp()
    def test_check_details_dict_False(self):
        self.assertEqual(self.app.check_details_dict({}), False)
    def test_check_details_dict_True(self):
        self.assertEqual(self.app.check_details_dict({'Lada': 'Блок управления отопителем (печкой) ВАЗ Lada Vesta 2015'}), True)