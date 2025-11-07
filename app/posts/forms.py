from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    TextAreaField, 
    SubmitField, 
    SelectField,
    BooleanField,
    DateTimeLocalField  
)
from wtforms.validators import (
    DataRequired, 
    Length
)
from datetime import datetime
from .models import PostCategory  

class PostForm(FlaskForm):
    """
    Форма для створення/редагування поста.
    """
    
    # title - StringField, required, max 150 (відповідає моделі)
    title = StringField(
        "Заголовок", 
        validators=[DataRequired(), Length(max=150)]
    )
    
    # content - TextAreaField, required
    content = TextAreaField(
        "Вміст", 
        validators=[DataRequired()]
    )
    
    # === ОСЬ ВИПРАВЛЕННЯ ===
    # Додаємо поле, яке вимагає модель
    author = StringField(
        'Автор', 
        validators=[DataRequired(), Length(max=20)], 
        default='Anonymous' # Значення за замовчуванням
    )
    # ======================
    
    # is_active (boolean)
    is_active = BooleanField(
        "Активний (відображається на сайті)", 
        default='checked'
    )
    
    # posted (DateTimeLocalField)
    posted = DateTimeLocalField(
        "Дата публікації",
        format='%Y-%m-%dT%H:%M',
        default=datetime.utcnow,
        validators=[DataRequired()]
    )
    
    # category (SelectField) - 'choices' генеруються з вашого Enum 'PostCategory'
    category = SelectField(
        "Категорія",
        choices=[(cat.value, cat.name.capitalize()) for cat in PostCategory],
        validators=[DataRequired()]
    )
    
    # submit
    submit = SubmitField("Створити пост")