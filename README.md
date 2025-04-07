# ToDo List task management service

## Требования к серверу
- Развёртывание проекта протестировано в среде:
  - **ОС**: Debian 12
  - **Docker**: 20.10.24
  - **Docker Compose**: 1.29.2

---

## Инструкция по запуску

### 1. Создание Telegram-бота
- С помощью Telegram-бота @BotFather выполните команду `/newbot` чтобы создать нового бота.
- Задайте имя и уникальный username для бота.
- Сохраните API token, предоставленный @BotFather для дальнейшей настройки.

### 2. Добавление команд боту
- В @BotFather выполните команду `/mybots`.
- Выберите созданного бота, нажмите **Edit Bot** → **Edit Commands**.
- Отправьте боту следующее сообщение:

```
tasks - Список задач
addtask - Добавить новую задачу
categories - Список категорий
addcategory - Добавить новую категорию
```

### 3. Клонирование проекта
- Подключитесь к серверу по SSH.
- Склонируйте проект с GitHub:

```bash
git clone https://github.com/kuzven/todolist.git
```

### 4. Перейдите в директорию проекта:

```bash
cd todolist
```

### 5. Создайте файл .env, используя шаблон .env.example:

```bash
cp .env.example .env
```

### 6. Настройка файла .env
- Откройте .env с помощью текстового редактора:

```bash
nano .env
```
- Сгенерируйте DJANGO_SECRET_KEY с помощью любого онлайн-генератора, например:

```
https://djecrety.ir/
```

- Скопируйте ключ и вставьте его в .env.
- Укажите значения для следующих параметров, например:

```
DJANGO_SECRET_KEY=n-v24$r$nmfhume8aeho@04nto(34$ir#_%4h1hx4xug&m71s7
DEBUG=False
ALLOWED_HOSTS=['localhost', 'web', '127.0.0.1', "213.180.204.11"]
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=securepassword
TELEGRAM_BOT_TOKEN=508627689:AAEuLPKs-EhrjrYGnz60bnYNZqakf6HJxc0
API_BASE_URL=http://213.180.204.11/api/
PG_DATABASE=todolist_db
PG_USER=todolist_user
PG_PASSWORD=todolist_password
```

### 7. Запуск Docker-контейнеров
- Соберите и запустите Docker-контейнеры:

```bash
docker-compose up --build -d
```
- Проверьте запущенные контейнеры:

```bash
docker ps
```

### 8. Проверка административной панели Django
- Для входа в административную панель перейдите по адресу:

```
http://your_vps_ip/admin
```

### 9. Проверка работы Telegram-бота
- Убедитесь, что бот функционирует корректно, отправив ему команды:

```
/start
/addcategory
/addtask
/categories
/tasks
```

### 10. Если возникнут трудности, проверьте логи контейнеров с помощью:

```bash
docker logs <container_name>
```
