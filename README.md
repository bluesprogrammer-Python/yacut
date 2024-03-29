# YaCut


### Описание
Сервис для создания коротких ссылок. Короткие ссылки ассоциируется с длинными
в базе данных и работают при помощи инструментов фреймворка. Можно создать короткую ссылку
самостоятельно или она будет сгенерирована автоматически при помощи рандомайзера.

### Технологии в проекте
	Flask 2.0.2, Jinja2 3.0.3, Sqlalchemy 1.4.29

### Инструкция по запуску
1. Установите и активируйте виртуальное окружение.
```bash
python -m venv venv
source venv/Scripts/./activate
```
2. Обновите менеджер пакетов pip и установите зависимости.
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```
3. Запустите проект.
```bash
flask run
```

Сайт доступен по ссылке: http://127.0.0.1:5000/

### Автор
Семёнов Сергей (Github - bluesprogrammer-Python, telegram - seregabrat9)
