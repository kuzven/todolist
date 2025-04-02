from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('telegram_id', 'telegram_username', 'first_name', 'last_name', 'is_active', 'is_staff')
    search_fields = ('telegram_id', 'telegram_username', 'first_name', 'last_name')
