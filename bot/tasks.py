import asyncio
from decouple import config
from aiogram import Bot
from celery import Celery

# Загружаем URL брокера из .env
BROKER_URL = config("CELERY_BROKER_URL")

# Создаём объект Celery
app = Celery('todolist', broker=BROKER_URL, backend=BROKER_URL)

@app.task
def notify_user(user_id, task_title):
    """
    Асинхронно отправляет уведомление пользователю при дедлайне задачи.
    """
    async def send_notification():
        try:
            # Создаём объект бота заново
            bot_token = config("TELEGRAM_BOT_TOKEN")  # Загружаем токен из .env
            bot = Bot(token=bot_token)

            message = (
                f"Напоминаем, что срок выполнения задачи '{task_title}' истёк!\n"
                "Вы можете:\n"
                "- Выполнить задачу.\n"
                "- Продлить срок выполнения."
            )
            await bot.send_message(chat_id=user_id, text=message)
            print(f"[INFO] Уведомление отправлено пользователю {user_id} для задачи '{task_title}'")
        except Exception as e:
            print(f"[ERROR] Ошибка при отправке уведомления: {e}")
        finally:
            await bot.session.close()  # Закрываем клиентскую сессию

    # Запуск асинхронной задачи
    asyncio.run(send_notification())
