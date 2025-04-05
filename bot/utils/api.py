import hashlib
import time
import aiohttp
from decouple import config

API_BASE_URL = config("API_BASE_URL")  # Загружаем значение из .env

async def get_tasks(user_id):
    """ Получает задачи через API """
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}tasks/?user_id={user_id}") as response:
            if response.status == 200:
                tasks = await response.json()
                print(f"[DEBUG] Полученные задачи: {tasks}")
                return tasks
            print(f"[DEBUG] Ошибка при загрузке задач: {response.status}")
            return None

async def create_task(user_id, title, description, category, due_date):
    """ Создаёт задачу через API и возвращает её данные """
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
            if response.status == 201:
                return await response.json()  # Возвращаем JSON-ответ
            return None  # Возвращаем None при ошибке

async def get_categories(user_id):
    """ Получает категории через API """
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}categories/?user_id={user_id}") as response:
            if response.status == 200:
                return await response.json()
            return None

async def create_category(user_id, name, description):
    """ Создает новую категорию через API """
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

async def update_task(task_id, is_completed):
    """ Обновляет задачу в базе данных """
    try:
        payload = {"is_completed": is_completed}
        print(f"[DEBUG] Отправляем данные для обновления задачи {task_id}: {payload}")  # Логируем данные

        async with aiohttp.ClientSession() as session:
            print(f"[DEBUG] Значение API_BASE_URL: {API_BASE_URL}")
            async with session.patch(f"{API_BASE_URL}tasks/{task_id}/", json=payload) as response:
                print(f"[DEBUG] Ответ API: Статус {response.status}, Тело {await response.text()}")
                if response.status == 200:
                    print(f"[INFO] Задача {task_id} успешно обновлена.")
                    return True
                else:
                    print(f"[ERROR] Ошибка при обновлении задачи {task_id}: {response.status}")
                    return False
    except Exception as e:
        print(f"[ERROR] Исключение при обновлении задачи {task_id}: {e}")
        return False
