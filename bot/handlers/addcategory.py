from aiogram import types, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.utils.api import create_category

# Состояния для добавления категории
class AddCategoryState(StatesGroup):
    name = State()
    description = State()

async def add_category_command(message: types.Message, state: FSMContext):
    await message.answer("Введите название категории:")
    await state.set_state(AddCategoryState.name)

async def process_category_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите описание категории:")
    await state.set_state(AddCategoryState.description)

async def process_category_description(message: types.Message, state: FSMContext):
    try:
        # Получаем данные из состояния
        user_data = await state.get_data()
        print(f"[DEBUG] Полученные данные от пользователя: {user_data}")
        
        # Получаем ID пользователя
        user = message.from_user.id
        print(f"[DEBUG] ID пользователя: {user}")

        # Вызываем create_category и передаём user
        response = await create_category(
            user,  # ID пользователя
            user_data['name'],  # Название категории
            message.text  # Описание категории
        )
        print(f"[DEBUG] Ответ от API create_category: {response}")

        # Проверяем результат
        if response:
            await message.answer(f"Категория '{user_data['name']}' добавлена.")
        else:
            await message.answer("Ошибка при добавлении категории.")
        await state.clear()
    except Exception as e:
        # Логируем исключение
        print(f"[ERROR] Ошибка в process_category_description: {e}")
        await message.answer("Ошибка при добавлении категории. Попробуйте позже.")

def register_handlers(dp: Dispatcher):
    dp.message.register(add_category_command, Command("addcategory"))
    dp.message.register(process_category_name, AddCategoryState.name)
    dp.message.register(process_category_description, AddCategoryState.description)
