from flask import Flask
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import InputRequired, Email
from hw2_validators import number_length, NumberLength

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test-secret-key'


class RegistrationForm(FlaskForm):
    email = StringField(validators=[
        InputRequired(message='Email обязателен'),
        Email(message='Неверный формат email')
    ])
    phone = IntegerField(validators=[
        InputRequired(message='Телефон обязателен'),
        NumberLength(10, 10, message='Телефон должен содержать 10 цифр')
    ])
    name = StringField(validators=[
        InputRequired(message='Имя обязательно')
    ])
    address = StringField(validators=[
        InputRequired(message='Адрес обязателен')
    ])
    index = IntegerField(validators=[
        InputRequired(message='Индекс обязателен')
    ])
    comment = StringField()


@app.route("/registration", methods=["POST"])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        email, phone = form.email.data, form.phone.data
        return f"Successfully registered user {email} with phone +7{phone}"
    return f"Invalid input, {form.errors}", 400


if __name__ == "__main__":
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
