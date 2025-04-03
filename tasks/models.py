from django.db import models
from users.models import BotUser


class Category(models.Model):
    id = models.CharField(primary_key=True, max_length=64)
    name = models.CharField(max_length=255, verbose_name="Название категории")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE, related_name="categories")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Task(models.Model):
    id = models.CharField(primary_key=True, max_length=64)
    title = models.CharField(max_length=255, verbose_name="Название задачи")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="tasks")
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE, related_name="tasks")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    due_date = models.DateTimeField(verbose_name="Срок выполнения")
    is_completed = models.BooleanField(default=False, verbose_name="Завершена ли задача")

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return self.title
