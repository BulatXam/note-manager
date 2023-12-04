""" Модуль, в котором хранятся все полезные многоразвые функции,
которые запускаются из команд.

Отдельно сами по себе они не могут существовать (!)

"""

import shutil
import os

from colorama import Fore
from pick import pick

from .models import Note


async def detail_note(note: Note):
    """ Вывод в консоли дополнительной информации заметки """
    print(cmd_title(note.title))
    print("\n")
    print(Fore.BLUE+f"{note.text}")

    input(
        "Введите Enter для выхода из режима "
        "просмотра детальной информации заметки."
    )


async def delete_note(note: Note):
    """ Вывод в консоли удаления заметки. """
    output = input("Введите y/n если действительно хотите удалить заметку: ")
    if output == "y" or output == "yes":
        await note.delete()
    else:
        input("Вы решили не удалять заметку! (Нажмите Enter, чтобы выйти)")


async def get_note(note: Note):
    """ Вывод действий над выбранной заметкой """
    command, index = pick(
        ["Детальная информация", "Удалить заметку", "Назад"],
        cmd_title("Выберите действие, которое надо совершить с заметкой")
    )

    match command:
        case "Детальная информация":
            await detail_note(note=note)
            await get_note(note=note)
        case "Удалить заметку":
            await delete_note(note=note)


def cmd_title(title: str):
    """ Вывод красивой заголовки <--  --> """
    os.system("cls")
    return f"<--       {title}       -->".center(
        shutil.get_terminal_size().columns
    )


# rulers 80
