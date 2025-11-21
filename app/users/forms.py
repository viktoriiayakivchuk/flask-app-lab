from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from app.users.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Ім\'я користувача', validators=[
        DataRequired(), 
        Length(min=4, max=20),
        Regexp(r'^[A-Za-z][A-Za-z0-9_.]*$', 
               message="Ім'я має починатися з літери і містити тільки літери, цифри, крапки або підкреслення")
    ])
    email = StringField('Email', validators=[
        DataRequired(), 
        Email()
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(), 
        Length(min=6)
    ])
    confirm_password = PasswordField('Підтвердіть пароль', validators=[
        DataRequired(), 
        EqualTo('password', message='Паролі повинні співпадати')
    ])
    submit = SubmitField('Зареєструватися')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Це ім\'я вже зайняте. Будь ласка, оберіть інше.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Цей email вже зареєстрований.')