import os
import django

# Устанавливаем переменную DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todolist.settings')

# Инициализируем Django
django.setup()

import asyncio
import logging
from aiogram import Bot, Dispatcher
from bot.bot import dp, bot
from bot.handlers import start, tasks, addtask, addcategory, categories

# Регистрация обработчиков
start.register_handlers(dp)
tasks.register_handlers(dp)
addtask.register_handlers(dp)
addcategory.register_handlers(dp)
categories.register_handlers(dp)

# Настройка логирования
logging.basicConfig(level=logging.INFO)

async def main():
    try:
        logging.info("Бот запускается...")
        await dp.start_polling(bot, skip_updates=True)
    except asyncio.CancelledError:
        print("Бот остановлен вручную.")

if __name__ == "__main__":
    asyncio.run(main())
