""" Entry point.

От сюда запускается наше приложение.
"""

import asyncio

from colorama import init
from tortoise.connection import connections

from src.db import database_init
from src.commands import start_menu


async def main():
    """ Точка входа. 
    
    Инициализируем все нужные инстурменты и запускаем командную строку.
    """
    init()
    await database_init()

    try:
        await start_menu()
    finally:
        # Если вручную не вырубить все коннекты к базе данных sqlite, 
        # то программа зависнет в конце выполнения.
        await connections.close_all(discard=True)


asyncio.run(main())


# rulers 80
