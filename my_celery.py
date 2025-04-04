from celery import Celery
from decouple import config

print("[DEBUG] my_celery.py загружен")

# Загружаем URL для брокера из .env
BROKER_URL = config("CELERY_BROKER_URL", default="redis://127.0.0.1:6379/0")
print(f"[DEBUG] Broker URL: {BROKER_URL}")

app = Celery('todolist', broker=BROKER_URL, backend=BROKER_URL)
app.autodiscover_tasks(['bot'])
