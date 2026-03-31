from datetime import datetime
from flask import Flask

app = Flask(__name__)
WEEKDAYS = ('понедельника', 'вторника', 'среды', 'четверга', 'пятницы', 'субботы', 'воскресенья')

@app.route('/hello-world/<name>')
def hello_world(name):
    num = datetime.today().weekday()
    day = WEEKDAYS[num]
    txt = 'Хорошей' if num in (2, 4, 5) else 'Хорошего'
    return f'Привет, {name}. {txt} {day}!'

if __name__ == '__main__':
    app.run(debug=True)

