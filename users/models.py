from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    telegram_id = models.BigIntegerField(unique=True, null=False, verbose_name="Telegram ID")
    telegram_username = models.CharField(max_length=255, blank=True, null=True, verbose_name="Telegram Username")
    first_name = models.CharField(max_length=255, verbose_name="First Name")
    last_name = models.CharField(max_length=255, verbose_name="Last Name")

    USERNAME_FIELD = 'telegram_id'
    REQUIRED_FIELDS = []  # Убираем стандартные обязательные поля

    def __str__(self):
        return f"{self.telegram_id} ({self.telegram_username})"
