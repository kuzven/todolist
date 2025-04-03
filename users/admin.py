from django.contrib import admin
from .models import User, BotUser

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser')

@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'telegram_username', 'first_name', 'last_name')
    search_fields = ('telegram_id', 'telegram_username', 'first_name', 'last_name')
