from datetime import datetime
import pytz
from aiogram import types, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.utils.api import get_categories, create_task
from bot.tasks import notify_user

# Указываем часовой пояс, используемый в Django
DJANGO_TIME_ZONE = pytz.timezone("America/Adak")

# Состояния для создания задачи
class AddTaskState(StatesGroup):
    category = State()
    title = State()
    description = State()
    due_date = State()

async def add_task_command(message: types.Message, state: FSMContext):
    try:
        # Получаем категории через API
        categories = await get_categories(message.from_user.id)
        print(f"[DEBUG] Полученные категории: {categories}")  # Логируем результат
        if not categories:
            await message.answer("У вас нет доступных категорий. Пожалуйста, создайте категорию с помощью /addcategory.")
            return

        # Формируем клавиатуру для выбора категории
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[])
        for category in categories:
            keyboard.keyboard.append([KeyboardButton(text=category["name"])])

        await message.answer("Выберите категорию для задачи:", reply_markup=keyboard)
        await state.set_state(AddTaskState.category)
    except Exception as e:
        print(f"[ERROR] Ошибка при обработке команды /addtask: {e}")
        await message.answer("Произошла ошибка. Попробуйте позже.")

async def process_category(message: types.Message, state: FSMContext):
    try:
        # Получаем категории через API
        categories = await get_categories(message.from_user.id)
        # Сопоставляем введённое пользователем название категории с её id
        category = next((c for c in categories if c["name"] == message.text), None)
        
        if category:
            # Сохраняем ID категории в состоянии
            await state.update_data(category=category["id"])
            await message.answer("Введите название задачи:")
            await state.set_state(AddTaskState.title)
        else:
            await message.answer("Выбранная категория не найдена. Попробуйте ещё раз.")
    except Exception as e:
        print(f"[ERROR] Ошибка при обработке категории: {e}")
        await message.answer("Произошла ошибка. Попробуйте позже.")

async def process_title(message: types.Message, state: FSMContext):
    try:
        # Получаем текущие данные из состояния
        data = await state.get_data()
        # Обновляем данные в состоянии
        await state.update_data(title=message.text)

        await message.answer("Введите описание задачи:")
        await state.set_state(AddTaskState.description)
    except Exception as e:
        print(f"[ERROR] Ошибка при обработке названия задачи: {e}")
        await message.answer("Произошла ошибка. Попробуйте позже.")

async def process_description(message: types.Message, state: FSMContext):
    try:
        # Обновляем данные в состоянии
        await state.update_data(description=message.text)

        await message.answer("Введите дату и время выполнения задачи в формате 'YYYY-MM-DD HH:MM':")
        await state.set_state(AddTaskState.due_date)
    except Exception as e:
        print(f"[ERROR] Ошибка при обработке описания задачи: {e}")
        await message.answer("Произошла ошибка. Попробуйте позже.")

async def process_due_date(message: types.Message, state: FSMContext):
    try:
        # Получаем текущую дату и время в зоне Django
        current_time = datetime.now(DJANGO_TIME_ZONE)
        print(f"[DEBUG] Текущее время (в зоне {DJANGO_TIME_ZONE}): {current_time}")

        # Проверяем, корректен ли формат даты
        due_date = datetime.strptime(message.text.strip(), "%Y-%m-%d %H:%M")
        due_date = DJANGO_TIME_ZONE.localize(due_date)  # Приводим дедлайн к часовому поясу Django

        if due_date < current_time:
            # Если дата в прошлом, возвращаем сообщение об ошибке
            await message.answer(
                "Введённые дата и время уже истекли. Введите корректные дату и время выполнения задачи в формате 'YYYY-MM-DD HH:MM':"
            )
            return
        
        # Сохраняем дату дедлайна и создаём задачу
        user_data = await state.get_data()
        print(f"[DEBUG] Данные пользователя для создания задачи: {user_data}")
        response = await create_task(
            user_id=message.from_user.id,
            title=user_data['title'],
            description=user_data['description'],
            category=user_data['category'],
            due_date=due_date.isoformat() # Сохраняем дату в ISO-формате
        )

        if response:
            # Запускаем задачу Celery для уведомления при дедлайне
            delay = (due_date - current_time).total_seconds()
            notify_user.apply_async(args=[message.from_user.id, user_data['title'], response["id"]], countdown=delay)
            print(f"[INFO] Задача для уведомления Celery создана. Задержка: {delay} секунд.")

            await message.answer(f"Задача '{user_data['title']}' добавлена с дедлайном {message.text}.")
        else:
            await message.answer("Ошибка при добавлении задачи.")
            print("[ERROR] create_task вернул None. Проверь API.")

        await state.clear()

    except ValueError:
        await message.answer(
            "Некорректный формат даты. Введите корректные дату и время выполнения задачи в формате 'YYYY-MM-DD HH:MM':"
        )
    except Exception as e:
        print(f"[ERROR] Ошибка при добавлении задачи: {e}")
        await message.answer("Произошла ошибка. Попробуйте позже.")

def register_handlers(dp: Dispatcher):
    dp.message.register(add_task_command, Command("addtask"))
    dp.message.register(process_category, AddTaskState.category)
    dp.message.register(process_title, AddTaskState.title)
    dp.message.register(process_description, AddTaskState.description)
    dp.message.register(process_due_date, AddTaskState.due_date)
