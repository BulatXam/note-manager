""" Утилиты для работы с настройками базы данных. """

from tortoise import Tortoise

from .config import TORTOISE_ORM


async def database_init(generate_schemas: bool = False) -> None:
    await Tortoise.init(TORTOISE_ORM)

    if generate_schemas:
        await Tortoise.generate_schemas()


# rulers 80
