# Дипломный проект

Этот проект представляет собой веб-приложение, разработанное с использованием Django.

## Требования

- Python 3.x
- pip (менеджер пакетов Python)
- Git

## Установка

1. Клонируйте репозиторий:
```bash
git clone <url-вашего-репозитория>
cd diplom-21
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
```

3. Активируйте виртуальное окружение:
- Для Windows:
```bash
venv\Scripts\activate
```
- Для Linux/Mac:
```bash
source venv/bin/activate
```

4. Установите зависимости:
```bash
pip install -r requirements.txt
```

5. Примените миграции базы данных:
```bash
python manage.py migrate
```

## Запуск проекта

### Вариант 1: Использование скрипта run.sh
```bash
./run.sh
```

### Вариант 2: Ручной запуск
1. Активируйте виртуальное окружение (если еще не активировано)
2. Запустите сервер разработки:
```bash
python manage.py runserver
```

После запуска приложение будет доступно по адресу: http://127.0.0.1:8000/

## Структура проекта

- `core/` - основные настройки проекта
- `courses/` - модуль для работы с курсами
- `users/` - модуль для работы с пользователями
- `templates/` - HTML шаблоны
- `media/` - медиафайлы
- `db.sqlite3` - база данных SQLite

## Используемые технологии

- Django 4.2+
- django-crispy-forms
- crispy-bootstrap5 