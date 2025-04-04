from aiogram import types, Dispatcher
from bot.utils.api import get_categories

async def categories_command(message: types.Message):
    categories = await get_categories(message.from_user.id)
    if categories:
        response = "\n".join([f"- {category['name']}: {category['description']}" for category in categories])
        await message.answer(f"Ваши категории:\n{response}")
    else:
        await message.answer("У вас пока нет категорий.")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(categories_command, commands=["categories"])
