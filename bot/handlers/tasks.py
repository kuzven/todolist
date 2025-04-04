from aiogram import types, Dispatcher
from aiogram.filters import Command
from bot.utils.api import get_categories, get_tasks


async def tasks_command(message: types.Message):
    try:
        # Получаем задачи пользователя
        tasks = await get_tasks(message.from_user.id)
        print(f"[DEBUG] Полученные задачи: {tasks}")

        if not tasks or len(tasks) == 0:
            await message.answer("Список задач пока пуст!")
            return

        # Получаем категории пользователя
        categories = await get_categories(message.from_user.id)
        print(f"[DEBUG] Полученные категории: {categories}")

        # Создаём словарь для быстрого поиска названий категорий по ID
        category_names = {category["id"]: category["name"] for category in categories}

        # Формируем сообщение со списком задач
        tasks_text = "Ваши задачи:\n\n" + "\n\n".join(
            [
                f"- {task['title']} (Категория: {category_names.get(task['category'], 'Без категории')}, "
                f"Дедлайн: {task['due_date']})"
                for task in tasks
            ]
        )
        await message.answer(tasks_text)
    except Exception as e:
        print(f"[ERROR] Ошибка при обработке команды /tasks: {e}")
        await message.answer("Произошла ошибка. Попробуйте позже.")

def register_handlers(dp: Dispatcher):
    dp.message.register(tasks_command, Command("tasks"))
