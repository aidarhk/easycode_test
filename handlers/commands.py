import asyncio
import logging

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from database import *
from services.validator import *

db = DataBase()
cr = Router()

logger = logging.getLogger(__name__)

class BirthdayStates(StatesGroup):
    waiting_name = State()
    waiting_date = State()

# Команда /start
@cr.message(Command('start'))
async def start_handler(message: Message):
    await message.answer(
        "Привет! Я бот для дней рождения.\n"
        "Команды:\n"
        "/add - добавить ДР (имя дата)\n"
        "/list - список ДР\n"
        "/delete имя - удалить\n"
        "/help - помощь"
    )

# Команда /help
@cr.message(Command('help'))
async def help_handler(message: Message):
    await message.answer(
        "/add Имя ДД.ММ - добавить\n"
        "/list - просмотреть\n"
        "/delete Имя - удалить\n"
        "Напоминания за 3 дня до ДР!"
    )

# Команда /add
@cr.message(Command('add'))
async def add_handler(message: Message, state: FSMContext):
    parts = message.text.split()

    if len(parts) != 3:
        await message.answer("Формат: /add Имя ДД.ММ (например, /add Иван 15.03)")
        return

    name = parts[1].strip()
    date_str = parts[2].strip()
    validated_date = validate_date(date_str)

    if not validated_date or not name:
        await message.answer("Ошибка: неверная дата (ДД.ММ или ДД/ММ) или пустое имя.")
        return

    db.add_birthday(message.from_user.id, name, validated_date)

    await message.answer(f"Добавлен: {name} - {validated_date[5:]}")

# Команда /list
@cr.message(Command('list'))
async def list_handler(message: Message):
    birthdays = db.get_birthdays(message.from_user.id)

    if not birthdays:
        await message.answer("Список пуст.")
        return

    text = "Ваши ДР:\n"
    for b in birthdays:
        text += f"• {b['name']}: {b['birth_date'][5:]}\n"
    await message.answer(text)

# Команда /delete
@cr.message(Command('delete'))
async def delete_handler(message: Message):
    parts = message.text.split(maxsplit=1)

    if len(parts) < 2:
        await message.answer("Формат: /delete Имя")
        return

    name = parts[1].strip()
    if db.delete_birthday(message.from_user.id, name):
        await message.answer(f"Удален: {name}")
    else:
        await message.answer(f"Не найдено: {name}")
