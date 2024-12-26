"""
Настройка Celery для проекта recipesite.
"""
import os
from celery import Celery

# Устанавливаем настройки Django для Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipesite.settings')

app = Celery('recipesite')

# Загрузка конфигурации из Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# # Автоматически находим задачи в приложениях Django
app.autodiscover_tasks()

