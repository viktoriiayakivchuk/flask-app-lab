from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    TextAreaField, 
    SubmitField, 
    SelectField, 
    BooleanField,
    DateTimeLocalField,
    SelectMultipleField 
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
    
    title = StringField(
        "Заголовок", 
        validators=[DataRequired(), Length(max=150)]
    )
    
    content = TextAreaField(
        "Вміст", 
        validators=[DataRequired()]
    )
    
    author_id = SelectField(
        "Автор", 
        coerce=int,
        validators=[DataRequired(message="Будь ласка, оберіть автора")]
    )
    
    # НОВЕ ПОЛЕ
    tags = SelectMultipleField(
        "Теги (утримуйте Ctrl/Cmd для вибору декількох)", 
        coerce=int
    )
    
    is_active = BooleanField(
        "Активний (відображається на сайті)", 
        default='checked'
    )
    
    posted = DateTimeLocalField(
        "Дата публікації",
        format='%Y-%m-%dT%H:%M',
        default=datetime.utcnow,
        validators=[DataRequired()]
    )
    
    category = SelectField(
        "Категорія",
        choices=[(cat.value, cat.name.capitalize()) for cat in PostCategory],
        validators=[DataRequired()]
    )
    
    submit = SubmitField("Створити пост")