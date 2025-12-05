from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class ExpenseForm(FlaskForm):
    title = StringField('Призначення', validators=[DataRequired(message="Введіть опис витрати")])
    
    amount = FloatField('Сума (грн)', validators=[
        DataRequired(message="Введіть суму"),
        NumberRange(min=0.01, message="Сума має бути додатною")
    ])
    
    category = SelectField('Категорія', coerce=int, validators=[DataRequired()])
    
    submit = SubmitField('Зберегти')