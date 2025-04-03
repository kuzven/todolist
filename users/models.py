from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Meta:
        verbose_name = "Пользователь Django"
        verbose_name_plural = "Пользователи Django"

class BotUser(models.Model):
    telegram_id = models.BigIntegerField(unique=True, null=False, verbose_name="Telegram ID")
    telegram_username = models.CharField(max_length=255, blank=True, null=True, verbose_name="Telegram Username")
    first_name = models.CharField(max_length=255, verbose_name="First Name")
    last_name = models.CharField(max_length=255, verbose_name="Last Name")

    class Meta:
        verbose_name = "Пользователь бота"
        verbose_name_plural = "Пользователи бота"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.telegram_id})"
