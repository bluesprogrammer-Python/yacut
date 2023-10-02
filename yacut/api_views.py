import re
from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from werkzeug.routing import BaseConverter
from .models import URLMap
from urllib.parse import urljoin
from .views import get_unique_short_id


PATTERN = r'[а-яА-ЯеёЁ\W]'

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter


@app.route('/api/id/<regex("[a-zA-Z0-9].*"):uuid>/', methods=['GET'])
def update_opinion(uuid):
    url = URLMap.query.filter_by(short=uuid).first()
    if url:
        return jsonify({'url': url.original}), 200
    else:
        raise InvalidAPIUsage('Указанный id не найден')


@app.route('/api/id/', methods=['POST'])
def create_url():
    url_map = URLMap()
    data = request.get_json()

    """Проверка на пустое тело запроса"""
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    
    """Проверка на наличие ключа url"""
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    long_url = data['url']

    """Проверка на наличие ключа custom_id"""
    if 'custom_id' not in data or data['custom_id'] is None:
        short_url = get_unique_short_id()
    else:
        short_url = data['custom_id']

        """Проверка содержания короткой ссылки"""
        check = re.search(PATTERN, short_url)
        if check:
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        if len(short_url) > 16:
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    """Проверка заполнения поля url"""
    if not long_url:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    
    """Проверка наличия короткой ссылки в БД"""
    if URLMap.query.filter_by(short=short_url).first():
        raise InvalidAPIUsage(f'Имя "{short_url}" уже занято.')
    
    url_map = URLMap(
        original=long_url,
        short=short_url
    )
    db.session.add(url_map)
    db.session.commit()
    absolute = request.url_root
    base_url = urljoin(absolute, short_url)
    return jsonify({'url': url_map.original, 'short_link': base_url}), 201


    """Проверка наличия длинной ссылке в БД
    check_long_url = URLMap.query.filter_by(original=long_url).first()
    if check_long_url:
        raise InvalidAPIUsage(f'Имя {check_long_url.short} уже занято.')"""