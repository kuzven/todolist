# Generated by Django 4.2.20 on 2025-04-03 06:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_botuser_remove_user_telegram_id_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='botuser',
            options={'verbose_name': 'Пользователь бота', 'verbose_name_plural': 'Пользователи бота'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Пользователь Django', 'verbose_name_plural': 'Пользователи Django'},
        ),
    ]
