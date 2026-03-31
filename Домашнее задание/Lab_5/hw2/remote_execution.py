from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, ValidationError
import subprocess

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test-secret-key'


def code_validator(form: FlaskForm, field: StringField):
    if not field.data:
        raise ValidationError('Код не может быть пустым')
    dangerous_patterns = ['|', '&', '`', '$', '>', '<', '\n', '\r']
    for pattern in dangerous_patterns:
        if pattern in field.data:
            raise ValidationError('Небезопасные символы в коде')


def timeout_validator(form: FlaskForm, field: IntegerField):
    if field.data is None:
        raise ValidationError('Тайм-аут обязателен')
    if not isinstance(field.data, int) or field.data <= 0:
        raise ValidationError('Тайм-аут должен быть положительным числом')
    if field.data > 30:
        raise ValidationError('Тайм-аут не может превышать 30 секунд')


class CodeForm(FlaskForm):
    code = StringField(validators=[InputRequired(message='Код обязателен'), code_validator])
    timeout = IntegerField(validators=[InputRequired(message='Тайм-аут обязателен'), timeout_validator])


def run_python_code_in_subprocess(code: str, timeout: int) -> str:
    command = [
        'prlimit',
        '--nproc=1:1',
        '--nofile=100:100',
        'python3',
        '-c',
        code
    ]

    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        try:
            stdout, stderr = process.communicate(timeout=timeout)
            if stdout:
                return stdout.strip()
            elif stderr:
                return f"Error: {stderr.strip()}"
            else:
                return "Код успешно выполнен (нет вывода)"

        except subprocess.TimeoutExpired:
            process.kill()
            process.communicate()
            return "Execution timeout: код не был выполнен в течение указанного времени"

    except Exception as e:
        return f"Execution error: {str(e)}"


@app.route('/run_code', methods=['POST'])
def run_code():
    form = CodeForm()
    if form.validate_on_submit():
        code = form.code.data
        timeout = form.timeout.data
        result = run_python_code_in_subprocess(code, timeout)
        return f"<pre>{result}</pre>", 200
    return f"Invalid input: {form.errors}", 400


if __name__ == '__main__':
    app.run(debug=True)
