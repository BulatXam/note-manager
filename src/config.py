""" Конфигурация проекта.

Здесь будут храниться константы и другие необходимые данные, 
общие для всего проекта
"""

DB_URL = 'sqlite://sqlite3.db'

TORTOISE_ORM = {
    "connections": {"default": DB_URL},
    "apps": {
        "models": {
            "models": ["src.models"],
            "default_connection": "default",
        },
    },
    'use_tz': False,
    'timezone': 'Europe/Moscow'
}


# rulers 80
