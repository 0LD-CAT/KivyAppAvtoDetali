import unittest

from AppAvtoDetali import ShopDetailsApp

class TestShopDetailsApp(unittest.TestCase):
    def setUp(self):
        self.app = ShopDetailsApp()
    def test_read_data_csv(self):
        test_Lada = {'Блок управления отопителем (печкой) ВАЗ Lada Vesta 2015': 10000, 'Задний бампер в цвет Лада Веста': 5000, 'Порог кузовной': 3600, 'Балка задняя ВАЗ Lada Kalina': 10000, 'Двигатель (ДВС) ВАЗ Lada Largus 2012': 100000, 'Блок ABS (насос) ВАЗ Lada Largus 2012': 10000, 'Фара левая ВАЗ Lada Vesta 2015': 11000, 'Диски ВАЗ (LADA) R13': 16000}
        test_BMW = {'Двигатель B57D30 BMW X3 G01 3.0': 244000, 'Камера BMW X5 (F15)': 16000, 'Магнитола BMW X5 (F15)': 15000, 'Вентилятор радиатора BMW X5 (F15)': 27000}
        test_Mazda = {'Турбина ДВС F6JA DV4TD 0375G9': 18600, 'Капот Mazda Mazda 6 (GH)': 14000, 'АКПП Mazda 3': 50000, 'Фара правая Mazda CX-5 II': 35000}
        test_Mercedes = {'Тормозные колодки задние ATE 13.0460-4064.2 Mercedes': 2000, 'Рейка рулевая Mercedes-Benz GLK-Class': 90000, 'Кулиса КПП Mercedes-Benz GLE-Class': 15000, 'Дверь задняя правая Mercedes-Benz GLS-Class': 25000}
        test_Volvo = {'Катализатор Volvo XC90 II': 65000, 'Трубка пластиковая Volvo XC90 II': 10000, 'Капот Volvo XC90 II': 80000, 'Балка подмоторная Volvo XC90': 40000}
        test_Honda = {'Коллектор выпускной Honda CR-V IV': 80000, 'Кулак поворотный передний правый Honda CR-V IV': 12000, 'Рейка рулевая Honda CR-V IV': 30000, 'Опора двигателя Honda CR-V IV': 13000}
        # Вызов метода для чтения данных из CSV
        self.app.read_data_csv()
        # Проверяем, что данные были загружены корректно
        self.assertEqual(self.app.DetaliForLada, test_Lada)
        self.assertEqual(self.app.DetaliForBMW, test_BMW)
        self.assertEqual(self.app.DetaliForMazda, test_Mazda)
        self.assertEqual(self.app.DetaliForMercedes, test_Mercedes)
        self.assertEqual(self.app.DetaliForVolvo, test_Volvo)
        self.assertEqual(self.app.DetaliForHonda, test_Honda)
        result = self.app.read_data_csv()
        self.assertEqual(result, None)

if __name__ == '__main__':
    unittest.main()