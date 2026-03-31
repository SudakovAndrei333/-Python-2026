from typing import Optional
from flask_wtf import FlaskForm
from wtforms import Field
from wtforms.validators import ValidationError


def number_length(min: int, max: int, message: Optional[str] = None):
    def _number_length(form: FlaskForm, field: Field):
        if field.data is None:
            return

        value_str = str(abs(int(field.data)))
        length = len(value_str)

        if not (min <= length <= max):
            if message is None:
                message = f'Длина числа должна быть от {min} до {max} цифр, сейчас {length}'
            raise ValidationError(message)

    return _number_length


class NumberLength:
    def __init__(self, min: int, max: int, message: Optional[str] = None):
        self.min = min
        self.max = max
        self.message = message

    def __call__(self, form: FlaskForm, field: Field):
        if field.data is None:
            return

        value_str = str(abs(int(field.data)))
        length = len(value_str)

        if not (self.min <= length <= self.max):
            if self.message is None:
                message = f'Длина числа должна быть от {self.min} до {self.max} цифр, сейчас {length}'
            else:
                message = self.message
            raise ValidationError(message)

if __name__ == "__main__":
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
