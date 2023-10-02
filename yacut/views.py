import string   
import random
from flask import Markup
from urllib.parse import urljoin

from flask import render_template, flash, redirect, abort
from werkzeug.routing import BaseConverter

from . import app, db
from .forms import URLMapForm
from .models import URLMap


MY_URL = 'http://127.0.0.1:5000/'


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


def get_unique_short_id():
    random_six = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=6))
    return random_six


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    url_map = URLMap()
    if form.validate_on_submit():
        original = form.original_link.data
        short_url = form.custom_id.data
        if not short_url:
            short_url = get_unique_short_id()

        """Проверки на наличие элементов в БД"""
        long_url = URLMap.query.filter_by(original=original).first()
        if long_url:
            base_url = urljoin(MY_URL, long_url.short + '/')
            flash(Markup(f'Для такого URL уже есть короткая ссылка: <a href="{base_url}">{base_url}</a>'))
            return render_template('url_creator.html', form=form)
        if URLMap.query.filter_by(short=short_url).first():
            flash('Такая короткая ссылка уже есть в БД, введите другое значение.')
            return render_template('url_creator.html', form=form)
        url_map = URLMap(
            original=original,
            short=short_url
        )
        db.session.add(url_map)
        db.session.commit()
        base_url = urljoin(MY_URL, short_url + '/')
        flash(Markup(f'Ваша новая ссылка готова: <a href="{base_url}">{base_url}</a>'))
    return render_template('url_creator.html', form=form, id=url_map.id)


app.url_map.converters['regex'] = RegexConverter


@app.route('/<regex("[a-zA-Z0-9].*"):uuid>/')
def url(uuid):
    model_url = URLMap.query.filter_by(short=uuid).first()
    if model_url:
        return redirect(model_url.original)
    else:
        return abort(404)
