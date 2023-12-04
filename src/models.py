""" Модели для работы с базой данных """

from tortoise import fields
from tortoise.models import Model


class Note(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=3000, unique=True)
    text = fields.TextField()


# rulers 80
