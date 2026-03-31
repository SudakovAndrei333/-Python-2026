import os
from flask import Flask

app = Flask(__name__)

@app.route('/head_file/<int:size>/<path:rel_path>')
def head_file(size, rel_path):
    dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(dir, rel_path)
    abs_path = os.path.abspath(path)

    if not os.path.exists(abs_path):
        return 'Файл не найден', 404
    if not os.path.isfile(abs_path):
        return 'Путь ведёт не к файлу', 400

    try:
        with open(abs_path, 'r', encoding='utf-8') as f:
            content = f.read(size)
    except Exception as e:
        return f'Ошибка чтения файла: {e}', 500

    result_size = len(content)
    return f'<b>{abs_path}</b> {result_size}<br>{content}'

if __name__ == '__main__':
    app.run(debug=True)

