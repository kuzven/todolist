from datetime import datetime
from aiogram import types, Dispatcher
from aiogram.filters import Command
from bot.utils.api import get_tasks, get_categories

async def tasks_command(message: types.Message):
    """
    Обрабатывает команду /tasks и возвращает список задач пользователя.
    """
    try:
        # Получаем задачи пользователя
        tasks = await get_tasks(message.from_user.id)
        if not tasks or len(tasks) == 0:
            await message.answer("Список задач пока пуст!")
            return

        # Оставляем только невыполненные задачи
        uncompleted_tasks = [task for task in tasks if not task['is_completed']]
        if not uncompleted_tasks:
            await message.answer("У вас нет невыполненных задач!")
            return

        # Получаем категории пользователя
        categories = await get_categories(message.from_user.id)
        category_names = {category["id"]: category["name"] for category in categories}

        # Формируем сообщение со списком задач
        tasks_text = "Ваши задачи:\n\n" + "\n\n".join([
            f"- Задача от {datetime.strptime(task['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z').strftime('%d-%m-%Y %H:%M')}\n"
            f"  Название: {task['title']}\n"
            f"  Категория: {category_names.get(task['category'], 'Неизвестная категория')}\n"
            f"  Описание: {task['description'] or 'Нет описания'}\n"
            f"  Срок выполнения: {datetime.strptime(task['due_date'], '%Y-%m-%dT%H:%M:%S%z').strftime('%d-%m-%Y %H:%M')}"
            for task in uncompleted_tasks
        ])

        await message.answer(tasks_text)
    except Exception as e:
        print(f"[ERROR] Ошибка при обработке команды /tasks: {e}")
        await message.answer("Произошла ошибка. Попробуйте позже.")

def register_handlers(dp: Dispatcher):
    """
    Регистрирует обработчики для задач.
    """
    dp.message.register(tasks_command, Command(commands=["tasks"]))  # Используем фильтр Command
