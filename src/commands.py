""" Исполнитель команд командной строки.

Здесь будут исполнение всех команд, командной строки.

"""

import os
import asyncio

from typing import List

from tortoise.expressions import Q
from tortoise.exceptions import IntegrityError
from pick import pick
from colorama import Fore

from .models import Note
from . import services


async def start_menu() -> None:
    """ Запускаем стартовое меню, в котором все необходимые главные функции. """
    title = services.cmd_title(
        "Выберите действие, которое Вы бы хотели совершить с заметками:"
    )

    commands = {
        "Добавить заметку": create_note,
        "Поиск заметки": search_note,
        "Удалить заметку": delete_note,
        "Все заметки": all_notes,
        "Выход": exit,
    }
    command, index = pick(list(commands.keys()), title)

    os.system("cls") # Очищаем консоль для красоты
    
    # Вместо кучу if или матч кейс юзаем словарь и экономим кучу строк
    await commands[command]()


async def create_note() -> None:
    """ Команда создания заметки 

    """
    print(services.cmd_title("Добавление заметки"))

    note_title = input(Fore.BLUE+"Введите заголовок заметки: "+Fore.GREEN)

    print(services.cmd_title(note_title))

    print(Fore.BLUE+"Введите заголовок заметки: "+Fore.GREEN+note_title)

    print(Fore.BLUE+"Введите содержание заметки: \n"+Fore.GREEN)
    note_text = input()

    try:
        await Note.create(
            title=note_title,
            text=note_text
        )
    except IntegrityError:
        print("Такая заметка уже существует! Введите заново название заметки!")
        await asyncio.sleep(5)
        await create_note()

    print(
        "Поздравляем! Вы создали заметку: " + 
        Fore.YELLOW + note_title + Fore.GREEN + "!"
    )

    await start_menu()


async def search_note(note_key_word: str|None = None) -> None:
    """ Команда поиска заметки 
    
    """
    print(services.cmd_title("Поиск заметки по ключевому слову"))
    
    if not note_key_word:
        note_key_word = input(
            Fore.BLUE + 
            "\nВведите ключевое слово, по которому мы найдем вашу заметку: " + 
            Fore.GREEN
        )

    notes = await Note.filter(
        Q(title__icontains=note_key_word) | Q(text__icontains=note_key_word)
    )

    notes_title = [note.title for note in notes]
    
    command, index = pick(
        [*notes_title, "Ввести заново", "Назад в меню"], 
        services.cmd_title("Поиск заметки по заголовку")
    )

    match command:
        case "Назад в меню":
            await start_menu()
        case "Ввести заново":
            await search_note()
        case _:
            await services.get_note(notes[index])

            await search_note(note_key_word=note_key_word)


async def all_notes() -> None:
    """Вывод всех заметок по выбору:
    
    """
    notes: List[Note] = await Note.all()
    notes_title = [f"{num}. {note.title}" for num, note in enumerate(notes)]

    command, index = pick(
        [*notes_title, "Назад в меню"], 
        services.cmd_title("Список все заметок")
    )

    if command == "Назад в меню":
        await start_menu()
    else:
        note: Note = notes[index]

        await services.get_note(note=note)

        await all_notes() # Возвращаемся обратно в список всех заметок


async def delete_note() -> None:
    """Удалить заметки. """
    notes: List[Note] = await Note.all()
    notes_title = [f"{num}. {note.title}" for num, note in enumerate(notes)]

    command, index = pick(
        [*notes_title, "Назад в меню"], 
        services.cmd_title("Выберите заметку, которую хотите удалить")
    )

    if command == "Назад в меню":
        await start_menu()
    else:
        await services.delete_note()

        await delete_note()


# rulers 80
