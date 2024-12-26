# pylint: skip-file
from .celery import app as celery_app  # Импортируем экземпляр Celery
__all__ = ('celery_app',)
