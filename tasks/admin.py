from django.contrib import admin
from .models import Category, Task

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name', 'user__telegram_username', 'user__first_name', 'user__last_name')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'due_date', 'is_completed')
    search_fields = ('title', 'user__telegram_username', 'user__first_name', 'user__last_name', 'category__name')
    list_filter = ('is_completed',)
