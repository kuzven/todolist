from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import Bot

# Функция отправки уведомления
async def send_task_notification(bot: Bot, task_id: str, user_id: int, task_data: dict):
    try:
        # Формируем кнопки
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton("Задача выполнена"))
        keyboard.add(KeyboardButton("Продлить срок выполнения"))

        # Текст уведомления
        notification_text = (
            f"Напоминание о задаче:\n\n"
            f"Название: {task_data['title']}\n"
            f"Категория: {task_data['category']}\n"
            f"Описание: {task_data['description'] or 'Нет описания'}\n"
            f"Срок выполнения: {task_data['due_date']}\n"
        )

        # Отправляем сообщение пользователю
        await bot.send_message(chat_id=user_id, text=notification_text, reply_markup=keyboard)
    except Exception as e:
        print(f"[ERROR] Ошибка при отправке уведомления: {e}")
