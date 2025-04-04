from aiogram import types, Dispatcher
from aiogram.filters import Command
from bot.utils.api import get_categories

async def categories_command(message: types.Message):
    """
    Отображает список категорий пользователя.
    """
    categories = await get_categories(message.from_user.id)
    if categories:
        response = "\n".join([f"- {category['name']}: {category['description']}" for category in categories])
        await message.answer(f"Ваши категории:\n{response}")
    else:
        await message.answer("У вас пока нет категорий.")

def register_handlers(dp: Dispatcher):
    dp.message.register(categories_command, Command(commands=["categories"]))  # Использование фильтра Command
