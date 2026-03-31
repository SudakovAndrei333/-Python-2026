import os
import random
import re
from datetime import datetime, timedelta
from flask import Flask

app = Flask(__name__)

cars_list = ['Chevrolet', 'Renault', 'Ford', 'Lada']
cats_lits = ['корниш-рекс', 'русская голубая', 'шотландская вислоухая', 'мейн-кун', 'манчкин']

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_FILE = os.path.join(BASE_DIR, 'war_and_peace.txt')

try:
    with open(BOOK_FILE, 'r', encoding='utf-8') as f:
        text = f.read()
    random_words = re.findall(r'[а-яА-Я]+', text)
except FileNotFoundError as e:
    random_words = []
    print(f"Файл war_and_peace.txt не найден! {e.args[0]}")

# счётчик посещений страницы /counter
def counter():
    counter.visits += 1
    return str(counter.visits)

counter.visits = 0

@app.route('/hello_world')
def hello_world():
    return 'Привет, мир!'

@app.route('/cars')
def cars():
    return ', '.join(cars_list)

@app.route('/cats')
def cats():
    return random.choice(cats_lits)

@app.route('/get_time/now')
def get_time_now():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f'Точное время: {current_time}'

@app.route('/get_time/future')
def get_time_future():
    future_time = (datetime.now() + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
    return f'Точное время через час будет {future_time}'

@app.route('/get_random_word')
def get_random_word():
    if not random_words:
        return 'Файл не найден или пуст'
    return random.choice(random_words)

@app.route('/counter')
def counter_route():
    return counter()

if __name__ == '__main__':
    app.run(debug=True)


