import asyncio
from decouple import config
from aiogram import Bot
from celery import Celery
from bot.utils.api import update_task


# Загружаем URL брокера из .env
BROKER_URL = config("CELERY_BROKER_URL")

# Создаём объект Celery
app = Celery('todolist', broker=BROKER_URL, backend=BROKER_URL)

@app.task
def notify_user(user_id, task_title, task_id):
    """
    Отправляет уведомление пользователю при дедлайне задачи
    """
    async def send_notification():
        try:
            # Создаём объект бота заново
            bot_token = config("TELEGRAM_BOT_TOKEN")  # Загружаем токен из .env
            bot = Bot(token=bot_token)

            # Обновляем статус задачи через API
            update_status = await update_task(task_id, is_completed=True)
            if not update_status:
                print(f"[ERROR] Не удалось обновить задачу {task_id}.")
                return

            # Текст сообщения
            message = (
                f"Напоминаем, что срок выполнения задачи '{task_title}' истёк и она помечена как выполненная!\n"
                "Если задача не выполнена, создайте новую задачу с желаемым сроком выполнения."
            )
            await bot.send_message(chat_id=user_id, text=message)
            print(f"[INFO] Уведомление отправлено пользователю {user_id} для задачи '{task_title}'")
        except Exception as e:
            print(f"[ERROR] Ошибка при отправке уведомления: {e}")
        finally:
            await bot.session.close()  # Закрываем клиентскую сессию

    # Запуск асинхронной задачи
    asyncio.run(send_notification())
