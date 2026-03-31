from datetime import datetime
from flask import Flask, abort

app = Flask(__name__)
WEEKDAYS = ('понедельника', 'вторника', 'среды', 'четверга', 'пятницы', 'субботы', 'воскресенья')


def _is_valid_name(name: str) -> bool:
    name = name.lower()
    patterns = [f'хорошего {day}' for day in WEEKDAYS] + \
                [f'хорошей {day}' for day in WEEKDAYS]
    return not any(pattern in name for pattern in patterns)


@app.route('/hello-world/<name>')
def hello_world(name):
    if not _is_valid_name(name):
        abort(400, description='Некорректное имя: не используйте пожелания вместо имени')

    num = datetime.today().weekday()
    day = WEEKDAYS[num]
    txt = 'Хорошей' if num in (2, 4, 5) else 'Хорошего'
    return f'Привет, {name}. {txt} {day}!'


if __name__ == '__main__':
    app.run(debug=True)

