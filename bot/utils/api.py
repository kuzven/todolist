import hashlib
import time
import aiohttp
from decouple import config

API_BASE_URL = config("API_BASE_URL")  # Загружаем значение из .env

async def get_tasks(user_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}tasks/?user_id={user_id}") as response:
            if response.status == 200:
                tasks = await response.json()
                print(f"[DEBUG] Полученные задачи: {tasks}")
                return tasks
            print(f"[DEBUG] Ошибка при загрузке задач: {response.status}")
            return None

async def create_task(user_id, title, description, category, due_date):
    # Генерация первичного ключа (pk) с помощью md5
    timestamp = int(time.time())  # Получаем текущее Unix-время
    unique_data = f"{user_id}_{title}_{timestamp}"  # Формируем уникальные данные
    pk = hashlib.md5(unique_data.encode()).hexdigest()  # Генерируем хеш

    payload = {
        "id": pk,  # Передаём pk, сгенерированный через md5
        "user": user_id,
        "category": category,
        "title": title,
        "description": description,
        "due_date": due_date
    }
    print(f"[DEBUG] Отправляем данные для создания задачи: {payload}")  # Логируем отправляемые данные

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_BASE_URL}tasks/", json=payload) as response:
            print(f"[DEBUG] Ответ API: Статус {response.status}, Тело {await response.text()}")
            return response.status == 201

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_BASE_URL}tasks/", json=payload) as response:
            print(f"[DEBUG] Ответ API: Статус {response.status}, Тело {await response.text()}")
            return response.status == 201

async def get_categories(user_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}categories/?user_id={user_id}") as response:
            if response.status == 200:
                return await response.json()
            return None

async def create_category(user_id, name, description):
    # Генерация первичного ключа (pk) с помощью md5
    timestamp = int(time.time()) # Получаем текущее Unix-время
    unique_data = f"{user_id}_{name}_{timestamp}" # Формируем уникальные данные
    pk = hashlib.md5(unique_data.encode()).hexdigest() # Генерируем хеш

    async with aiohttp.ClientSession() as session:
        payload = {
            "id": pk,  # Передаём pk, сгенерированный через md5
            "user": user_id,
            "name": name,
            "description": description
        }
        print(f"[DEBUG] Отправка данных: {payload}")  # Логируем отправляемый JSON
        async with session.post(f"{API_BASE_URL}categories/", json=payload) as response:
            print(f"[DEBUG] Статус ответа: {response.status}, Тело ответа: {await response.text()}")
            if response.status == 201:  # Успешное создание категории
                return True
            else:
                print(f"Ошибка API при добавлении категории: {response.status} - {await response.text()}")
                return False
