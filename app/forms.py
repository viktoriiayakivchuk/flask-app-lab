from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, SelectField, SubmitField, 
                   PasswordField, BooleanField) 
from wtforms.validators import DataRequired, Length, Email, Regexp

# === ЗАВДАННЯ 1 - ЛАБ 5====
class ContactForm(FlaskForm):
    """
    Форма для сторінки контактів (Завдання 1)
    """
    name = StringField('Ім\'я', 
                       validators=[DataRequired(message="Це поле обов'язкове"), 
                                   Length(min=4, max=10, message="Довжина має бути від 4 до 10 символів")])
    
    email = StringField('Email', 
                        validators=[DataRequired(message="Це поле обов'язкове"), 
                                    Email(message="Неправильний формат email")])
    
    phone = StringField('Телефон', 
                        validators=[DataRequired(message="Це поле обов'язкове"), 
                                    Regexp(r'^\+380\d{9}$', 
                                           message="Формат має бути +380xxxxxxxxx (12 цифр)")])
    
    subject_choices = [
        ('general', 'Загальне питання'),
        ('support', 'Технічна підтримка'),
        ('feedback', 'Відгук')
    ]
    subject = SelectField('Тема', 
                          choices=subject_choices, 
                          validators=[DataRequired(message="Будь ласка, оберіть тему")])
    
    message = TextAreaField('Повідомлення', 
                            validators=[DataRequired(message="Це поле обов'язкове"), 
                                        Length(max=500, message="Максимум 500 символів")])
    
    submit = SubmitField('Надіслати')

# === ЗАВДАННЯ 2 - ЛАБ 5===

class LoginForm(FlaskForm):
    """
    Форма для сторінки логіну (Завдання 2)
    """
    username = StringField('Ім\'я користувача',
                           validators=[DataRequired(message="Це поле обов'язкове")])
    
    password = PasswordField('Пароль',
                             validators=[DataRequired(message="Це поле обов'язкове"),
                                         Length(min=4, max=10, message="Пароль має бути від 4 до 10 символів")])
    
    remember_me = BooleanField('Запам\'ятати мене')
    
    submit = SubmitField('Ввійти')