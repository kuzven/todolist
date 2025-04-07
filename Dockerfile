FROM python:3.12-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean

# Установка зависимостей Python
WORKDIR /app
ENV PYTHONPATH=/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование приложения
COPY . .

# Команда запуска
CMD ["sh", "-c", "sleep 30 && python manage.py runserver 0.0.0.0:8000"]