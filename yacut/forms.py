from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, URLField
from wtforms.validators import DataRequired, Length, Optional, URL


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 256),
                    URL()]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(6), Optional()]
    )
    submit = SubmitField('Создать')
