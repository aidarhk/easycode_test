import asyncio
import logging
from datetime import date, timedelta

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database import *
from handlers import commands
from config_reader import config

logging.basicConfig(level=logging.INFO)

db = DataBase()

# Объект бота
bot = Bot(
    token=config.bot_token.get_secret_value()
)
dp = Dispatcher(storage=MemoryStorage())

@dp.error()
async def error_handler(event, exception):
    logging.error(f"Ошибка: {exception}")
    await bot.send_message(event.data.message.chat.id, "Произошла ошибка. Попробуйте позже.")

# Функция проверки напоминаний
async def check_reminders():
    today = date.today()
    remind_date = today + timedelta(days=3)

    rows = db.data_notif()

    for user_id, name, birth_str in rows:
        bdate = date.fromisoformat(birth_str)
        next_bday = date(remind_date.year, bdate.month, bdate.day)
        if next_bday == remind_date:
            await bot.send_message(
                user_id,
                f"🎉 Напоминание! День рождения {name} через 3 дня ({bdate.month:02d}.{bdate.day:02d})"
            )


# Запуск процесса поллинга новых апдейтов
async def main():
    # Логгирование
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # Диспетчер
    dp = Dispatcher()

    # Регистрация роутеров
    dp.include_routers(
        commands.cr
    )

    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_reminders, 'cron', hour=9, minute=0)  # Ежедневно в 9:00
    scheduler.start()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
