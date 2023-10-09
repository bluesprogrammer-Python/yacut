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
        custom_id = form.custom_id.data
        if not custom_id:
            custom_id = get_unique_short_id()

        """Проверка на наличие короткой ссылки в БД"""
        if URLMap.query.filter_by(short=custom_id).first():
            flash(f'Имя {custom_id} уже занято!')
            return render_template('url_creator.html', form=form)

        url_map = URLMap(
            original=original,
            short=custom_id
        )
        db.session.add(url_map)
        db.session.commit()
        absolute = request.url_root
        base_url = urljoin(absolute, custom_id)
        flash(Markup(f'Ваша новая ссылка готова: <a href="{base_url}">{base_url}</a>'))
    return render_template('url_creator.html', form=form, id=url_map.id)


@app.route('/<short_id>', methods=['GET'])
def url(short_id):
    model_url = URLMap.query.filter_by(short=short_id).first_or_404()
    if model_url:
        return redirect(model_url.original)
