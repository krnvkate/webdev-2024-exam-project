"""
Задачи для django проекта. Периодические задачи (celery)
"""
import logging
from datetime import timedelta

from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone

from .models import Recipe

logger = logging.getLogger(__name__)


@shared_task
def delete_unpopular_recipes():
    try:
        # Получаем дату, соответствующую "более года назад"
        one_year_ago = timezone.now() - timedelta(days=365)

        # Находим и удаляем рецепты
        recipes = Recipe.objects.filter(rating__lt=2, publish__lt=one_year_ago)
        count = recipes.count()
        for recipe in recipes:
            recipe.status = 'DT'  # Устанавливаем новый статус - Удалён
            recipe.save()  # Сохраняем изменения
            logger.info(f"Статус обновлён для рецепта с id {recipe.id} и названием {recipe.title}")
            # Проверяем, был ли статус обновлён
            updated_recipe = Recipe.objects.get(id=recipe.id)
            logger.info(f"Статус после сохранения: {updated_recipe.status}")

        logger.info(f"Успешно удалено {count} непопулярных рецепта(ов)")
        return f"Удалено {count} рецепта(ов)"
    except Exception as e:
        logger.error(f"Ошибка при удалении непопулярных рецептов: {str(e)}")
        raise


@shared_task
def notify_new_recipes():
    # Получаем дату, соответствующую неделе назад
    one_week_ago = timezone.now() - timedelta(days=7)

    # Находим новые рецепты, добавленные за последнюю неделю
    new_recipes = Recipe.objects.filter(publish__gte=one_week_ago)

    # Проверяем, есть ли новые рецепты
    if not new_recipes.exists():
        logger.info("Нет новых рецептов за последнюю неделю.")
        return "Нет новых рецептов."

    # Получаем всех пользователей
    users = User.objects.all()

    # Формируем и отправляем письма каждому пользователю
    for user in users:
        subject = "Уведомление о новых рецептах"
        message = "Здравствуйте!\n\nВот новые рецепты, которые были добавлены за последнюю неделю:\n"

        # Добавляем все новые рецепты в сообщение
        for recipe in new_recipes:
            message += f"- {recipe.title}\n"

        message += "\nС уважением,\nКоманда рецептов."

        # Отправка письма
        send_mail(
            subject,
            message,
            'sub_kate04@mail.com',  # Ваш адрес электронной почты
            [user.email],  # Адрес получателя
            fail_silently=False,
        )

        logger.info(f"Письмо отправлено на {user.email}")

    return f"Уведомления отправлены для {len(users)} пользователей."

