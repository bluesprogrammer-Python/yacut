import random
import string
from urllib.parse import urljoin

from flask import Markup, flash, redirect, render_template, request

from . import app, db
from .forms import URLMapForm
from .models import URLMap

URL_LENGTH = 6


def get_unique_short_id():
    random_six = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=URL_LENGTH))
    return random_six


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    url_map = URLMap()
    if form.validate_on_submit():
        original = form.original_link.data
        short_name = form.custom_id.data
        if not short_name:
            short_name = get_unique_short_id()

        """Проверка на наличие короткой ссылки в БД"""
        if URLMap.query.filter_by(short=short_name).first():
            flash(f'Предложенный вариант короткой ссылки уже существует.')
            return render_template('url_creator.html', form=form)

        url_map = URLMap(
            original=original,
            short=short_name
        )
        db.session.add(url_map)
        db.session.commit()
        absolute = request.url_root
        base_url = urljoin(absolute, short_name)
        flash(Markup(f'Ваша новая ссылка готова: <a href="{base_url}">{base_url}</a>'))
    return render_template('url_creator.html', form=form, id=url_map.id)


@app.route('/<short_id>', methods=['GET'])
def url(short_id):
    model_url = URLMap.query.filter_by(short=short_id).first_or_404()
    if model_url:
        return redirect(model_url.original)
