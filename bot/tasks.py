from bot import bot
from celery import Celery

app = Celery('todolist')

@app.task
def notify_user(user_id, task_title):
    """
    Отправляет уведомление пользователю о приближающемся дедлайне задачи.
    """
    try:
        message = (
            f"Напоминаем, что срок выполнения задачи '{task_title}' истёк или истекает!\n"
            "Вы можете:\n"
            "- Выполнить задачу.\n"
            "- Продлить срок выполнения."
        )
        bot.send_message(chat_id=user_id, text=message)
        print(f"[INFO] Уведомление отправлено пользователю {user_id} для задачи '{task_title}'")
    except Exception as e:
        print(f"[ERROR] Ошибка при отправке уведомления: {e}")
