from aiogram import types, Dispatcher
from aiogram.filters import Command
from asgiref.sync import sync_to_async
from users.models import BotUser


async def start_command(message: types.Message):
    try:
        # Обернём Django ORM в sync_to_async
        user, created = await sync_to_async(BotUser.objects.get_or_create)(
            telegram_id=message.from_user.id,  # Telegram ID
            defaults={
                "telegram_username": message.from_user.username,  # Username (может быть None)
                "first_name": message.from_user.first_name or "",  # Имя
                "last_name": message.from_user.last_name or ""  # Фамилия
            }
        )
        full_name = " ".join(filter(None, [user.first_name, user.last_name])).strip()
        if created:
            await message.answer(f"{full_name}! Добро пожаловать в телеграм-бот для управления задачами ToDo List. Отправьте /tasks для просмотра ваших задач.")
        else:
            await message.answer(f"С возвращением, {full_name}! Отправьте /tasks для просмотра ваших задач.")
    except Exception as e:
        # Обработка ошибок при регистрации
        await message.answer("Произошла ошибка при регистрации. Пожалуйста, попробуйте позже.")
        print(f"[ERROR] Ошибка при регистрации пользователя: {e}")


def register_handlers(dp: Dispatcher):
    dp.message.register(start_command, Command("start"))
