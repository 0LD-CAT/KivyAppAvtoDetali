import requests
from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
import csv
import flask

Window.size = (800, 500)
Window.set_title('Детали от поставщиков')
# Загружаем KV файл
Builder.load_file('login.kv')

class MainApp(App): # запуск окон приложения
    def build(self):
        return ScreenManagement()

class ScreenManagement(ScreenManager): # скрин менеджер для переключения окон
    pass

# Реализация Порождающего паттерна - Строитель
class OrderBuilder:
    def __init__(self, ShopDetails):
        self.order = ShopDetails

    def set_order_id(self):
        order_id = self.get_next_order_id('files/orders.csv')
        return order_id
    # определение id заказа
    def get_next_order_id(self, file_path):
        try:
            with open(file_path, 'r') as file:
                # Читаем первую строку и игнорируем её
                file.readline()

                # Инициализируем current_id
                current_id = 0
                # Считываем оставшиеся строки
                for line in file:
                    # Пробуем преобразовать строку в целое число
                    try:
                        order_id = int(line.split(',')[0].strip())
                        current_id = max(current_id, order_id)
                    except ValueError:
                        # Если не удалось преобразовать строку в число, игнорируем её
                        continue

        except FileNotFoundError:
            current_id = 0  # Если файл не существует, начинаем с 0

        return current_id + 1

    def set_user_phone(self):
        phone = self.order.UserPhone
        return phone

    def set_parts(self):
        parts = self.order.PurshParts
        return parts

    def set_total_price(self):
        total_price = self.order.total_price
        return total_price

    def set_way_delivery(self):
        way_delivery = type(self.order.delivery_strategy).__name__
        return way_delivery

    def create_order(self):
        order_id = self.set_order_id()
        user_phone = self.set_user_phone()
        parts = self.set_parts()
        total_sum = self.set_total_price()
        way_delivery = self.set_way_delivery()
        return (f'{order_id}, {user_phone}, {parts}, {total_sum}, {way_delivery}')

# Реализация Структурного паттерна - Компоновщик
class CarDetail: # Отдельная деталь автомобиля

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name} - {self.price} руб."

# Реализация Структурного паттерна - Компоновщик
class CarComposite: # Группа деталей для одной марки автомобиля

    def __init__(self):
        self.details = []

    def add_detail(self, detail): # Добавляет деталь
        self.details.append(detail)

    def remove_detail(self, detail): # Удаляет деталь
        self.details.remove(detail)

    def get_details(self): # Возвращает список всех деталей
        return self.details

# Реализация паттерна Поведения - Стратегия
class DeliveryStrategy:
    def calculate_cost(self, cost):
        pass

class StandardDelivery(DeliveryStrategy):
    def calculate_cost(self, cost):
        return cost + 1000

class ExpressDelivery(DeliveryStrategy):
    def calculate_cost(self, cost):
        return cost + 5000

class ShopDetailsApp(Screen): # Основное приложение магазина
    # репозиторий
    def __init__(self, **kwargs): # детали их стоимость и общая стоимость заказа
        super(ShopDetailsApp, self).__init__(**kwargs)
        self.car_composites = {
            "Lada": CarComposite(),
            "BMW": CarComposite(),
            "Mazda": CarComposite(),
            "Mercedes": CarComposite(),
            "Volvo": CarComposite(),
            "Honda": CarComposite()
        }
        self.read_data_csv()
        self.delivery_strategy = None
        self.UserPhone = None
        self.PurshParts = []
        self.total_price = 0
    # репозиторий
    def read_data_csv(self): # Чтение данных для деталей
        try:
            with open('files/details.csv', mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    car_brand = row[0]
                    part_name = row[1]
                    part_price = int(row[2])
                    if car_brand in self.car_composites:
                        detail = CarDetail(part_name, part_price)
                        self.car_composites[car_brand].add_detail(detail)
        except FileNotFoundError as e:
            print(e)
            return e
        return None

    # Сервис
    def DeliverySelect(self):
        spinner = self.ids.spinner2
        if spinner.text == "Стандарт - 1000руб.":
            self.delivery_strategy = StandardDelivery()
        elif spinner.text == "Экспресс - 5000руб.":
            self.delivery_strategy = ExpressDelivery()
        else:
            self.delivery_strategy = None

        print(f"Выбран способ доставки: {spinner.text}")

    # Сервис
    def on_spinner_select(self): # всплывающий выбор марки машины
        spinner = self.ids.spinner
        details_box = self.ids.details_box
        details_box.clear_widgets()
        details_dict = self.car_composites.get(spinner.text)

        if self.check_details_dict(details_dict):  # вывод деталей для марки машины
            for detail in details_dict.get_details():
                label = Label(text=str(detail), size_hint_y=None, height=40)
                button = Button(text='В корзину', size_hint_y=None, height=40, background_color=(0, 0, 1, 1))
                button.bind(on_press=lambda instance, part_name=detail.name, price=detail.price:
                self.add_to_cart(part_name, price))  # кнопка добавления в корзину

                details_box.add_widget(label)
                details_box.add_widget(button)

    def check_details_dict(self, details_dict):  # Проверка на пустоту
        return bool(details_dict)

    # Контроллер
    def add_to_cart(self, part_name, price): # добавление в корзину
        self.PurshParts.append(part_name)
        self.total_price += price
        cart_label = self.ids.cart_label
        cart_label.text = f'Корзина: {self.total_price} руб.'

    # Контроллер
    def clear_cart(self): # очистка корзины
        self.total_price = 0
        self.PurshParts.clear()
        cart_label = self.ids.cart_label
        cart_label.text = 'Корзина: 0 руб.'

    # Контроллер
    def calculate_total_cost(self):
        base_cost = self.total_price  # Основная стоимость заказа
        if self.delivery_strategy:
            total_cost = self.delivery_strategy.calculate_cost(base_cost)
            return total_cost
        else:
            return base_cost

    # Контроллер
    def payment(self): # оформление заказа
        if self.total_price > 0:
            total_cost = self.calculate_total_cost()
            if total_cost == self.total_price:
                print("Стратегия доставки не выбрана.")
            else:
                print(f'Заказ оформлен на сумму: {self.total_price} руб.\nСтоимость доставки: {total_cost - self.total_price}руб.\nИтого к оплате: {total_cost}')
                builder = OrderBuilder(self)
                order = builder.create_order()
                self.write_order(order) # запись заказа
                self.clear_cart() # очистка корзины
        else:
            print('Корзина пуста!')
    # Репозиторий
    def write_order(self, order):
        try:
            with open('files/orders.csv', mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                order = order.split(',')
                writer.writerow(order)  # запись данных в файл
                return True
        except FileNotFoundError as e:
            return e

    # Сервис
    def open_login_app(self):
        self.PurshParts.clear()
        self.clear_cart() # очищаем корзину перед выходом
        # Переключаемся на экран входа в приложение
        self.manager.current = 'login'


class LoginScreen(Screen): # окно входа
    # Контроллер
    def login(self):
        phone = self.ids.phone_input.text
        password = self.ids.password_input.text
        response = requests.post('http://127.0.0.1:5000/login', json={'phone': phone, 'password': password})
        result = response.json()['message']

        # Проверка на пустоту полей
        if result == 'Пожалуйста, заполните все поля.':
            self.show_error(result)
            return
        if result == 'Ошибка при чтении данных.': # Проверка на отсутствие данных
            self.show_error(result)
            return
        if result == True: # проверка на совпадение веденных пароля и номера телефона
            self.open_main_app(phone) # Переключаемся на основной экран приложения, если пароль и номер совпадают
            self.ids.password_input.text = ""  # Очистка поля ввода пароля
            self.ids.phone_input.text = ""  # Очистка поля ввода телефона
            return
        self.show_error(result)
        self.ids.password_input.text = ""


    # Контроллер
    def show_error(self, message):
        popup = Popup(title='Ошибка', content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    # Сервис
    def open_main_app(self, phone): # Переключение экрана
        main_app = self.manager.get_screen('main')
        if isinstance(main_app, ShopDetailsApp):
            main_app.UserPhone = phone  # Передаем номер телефона в основное приложение
        self.manager.current = 'main'  # Переключаемся на основной экран приложения



class RegisterScreen(Screen): # окно регистрации
    # Контроллер
    def register(self):
        phone = self.ids.phone_input.text
        password = self.ids.password_input.text
        response = requests.post('http://127.0.0.1:5000/registration', json={'phone': phone, 'password': password})
        result = response.json()['message']
        # Проверка на пустоту полей
        if result == 'Пожалуйста, заполните все поля.':
            self.show_error(result)
            return

        if result == "Этот номер телефона уже зарегистрирован.":
            self.show_error(result)
            self.ids.password_input.text = ""  # Очистка поля ввода пароля
            self.ids.phone_input.text = ""  # Очистка поля ввода телефона
            return

        if result == "Номер телефона должен состоять из 11 цифр и начинаться с 8 или 7!":  # проверка на уникальность, длину и цифры для номера
            self.ids.password_input.text = ""  # Очистка поля ввода пароля
            self.ids.phone_input.text = ""  # Очистка поля ввода телефона
            self.show_error(result)
            return

        if result == 'Регистрация успешна!':  # Проверка на успешность записи в файл
            self.success_reg(result)
            self.ids.password_input.text = ""  # Очистка поля ввода пароля
            self.ids.phone_input.text = ""  # Очистка поля ввода телефона
        else:
            self.ids.password_input.text = ""  # Очистка поля ввода пароля
            self.ids.phone_input.text = ""  # Очистка поля ввода телефона
            self.show_error(result)

    # Контроллер
    def show_error(self, message): # вывод ошибок
        popup = Popup(title='Ошибка', content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    # Контроллер
    def success_reg(self, message): # вывод сообщения об успешной регистрации
        popup = Popup(title='Регистрация', content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

if __name__ == "__main__": # запуск приложения
   MainApp().run()