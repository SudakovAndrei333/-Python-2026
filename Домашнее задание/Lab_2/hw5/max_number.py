from flask import Flask

app = Flask(__name__)

@app.route('/max_number/<path:numbers>')
def max_number(numbers):
    parts = numbers.split('/')
    valid = []
    for p in parts:
        try:
            valid.append(int(p))
        except ValueError:
            continue
    if not valid:
        return 'Не передано ни одного числа'
    max_val = max(valid)
    return f'Максимальное число: <i>{max_val}</i>'

if __name__ == '__main__':
    app.run(debug=True)

