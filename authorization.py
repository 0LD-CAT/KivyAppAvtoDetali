from flask import Flask, request, jsonify
import csv

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    phone = data.get('phone')
    password = data.get('password')

    if not phone or not password:
        return jsonify({'message': 'Пожалуйста, заполните все поля.'}), 401
    result = check_phone_pass(phone, password)
    if result is None:  # Проверка на отсутствие данных
        return jsonify({'message': 'Ошибка при чтении данных.'}), 401
    if result:  # проверка на совпадение веденных пароля и номера телефона
        return jsonify({'message': True}), 200
    return jsonify({'message': 'Неверный номер телефона или пароль.'}), 401


# Сервис
def check_phone_pass(phone, password):  # проверка на совпадение веденных пароля и номера телефона
    reader = read_login_csv()  # чтение данных для входа
    if reader is None:  # Проверка на отсутствие данных
        return None
    for row in reader:
        if row[0] == phone and row[1] == password:  # проверка на совпадение веденных пароля и номера телефона
            return True
    return False


# репозиторий
def read_login_csv(): # Чтение данных для входа
    try:
        with open('files/login.csv', mode='r') as file:
            reader = csv.reader(file)
            next(reader)
            return list(reader)
    except FileNotFoundError as e:
        print(e)
        return None

@app.route('/registration', methods=['POST'])
def register():
    data = request.json
    phone = data.get('phone')
    password = data.get('password')
    # Проверка на пустоту полей
    if not phone or not password:
        return jsonify({'message': 'Пожалуйста, заполните все поля.'}), 401

    if not is_phone_unique(phone):
        return jsonify({'message': 'Этот номер телефона уже зарегистрирован.'}), 401

    if not check_phone_num(phone):  # проверка на уникальность, длину и цифры для номера
        return jsonify({'message': 'Номер телефона должен состоять из 11 цифр и начинаться с 8 или 7!'}), 401
    result = write_log_csv(phone, password)
    if result is True:  # Проверка на успешность записи в файл
        return jsonify({'message': 'Регистрация успешна!'}), 200
    else:
        return jsonify({'message': result}), 401

    # репозиторий
def write_log_csv(phone, password): # запись в файл данных при регистрации
    try:
        with open('files/login.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([phone, password])  # запись данных в файл
            return True
    except FileNotFoundError as e:
        return e
    # Сервис
def check_phone_num (phone): # Проверка на длинну и цифры в телефоне
    if len(phone) == 11 and phone.isdigit() and (phone[0] == '8' or phone[0] == '7'):
        return True
    else:
        return False
# Сервис
def is_phone_unique(phone): # проверка на уникальность номера при регистрации
    reader = check_phone_inFile()
    if reader == []:  # Номер телефона уникален
        return True
    else:
        for row in reader:
            if row[0] == phone:
                return False  # Номер телефона уже существует
    return True
# Репозиторий
def check_phone_inFile(): # проверка
    try:
        with open('files/login.csv', mode='r') as file:
            reader = csv.reader(file)
            return list(reader)
    except FileNotFoundError:
        return []  # Если файл не найден, считаем номер уникальным

if __name__ == '__main__':
    app.run()