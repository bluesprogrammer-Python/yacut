from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    URL()]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Optional(),
                    Length(min=1, max=16)]
    )
    submit = SubmitField('Создать')
