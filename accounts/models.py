"""
Модели для профиля пользователя и любимых рецептов.
"""
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from simple_history import register
from simple_history.models import HistoricalRecords

from recipes.models import Recipe

register(User)


class Profile(models.Model):
    """Описание модели Пользователя"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                verbose_name="Пользователь")
    avatar = models.ImageField(upload_to='users_avatar', blank=True, verbose_name="Фото профиля")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    country = models.CharField(max_length=50, null=True, blank=True, verbose_name="Страна")
    city = models.CharField(max_length=50, null=True, blank=True, verbose_name="Город")
    info = models.TextField(null=True, blank=True, verbose_name="О себе")
    history = HistoricalRecords()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

# Сигналы на автоматическое создание и обновление, когда создаю или обновляю
# стандартную модель пользователя (User).


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """Сигнал на создание"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    """Сигнал на сохранение"""
    instance.profile.save()


class FavoriteRecipe(models.Model):
    """Описание модели с любимыми рецептами пользователей"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='like_recipe',
                             verbose_name="Пользователь")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='users_like',
                               verbose_name="Понравившийся рецепт")
    fav_date = models.DateField(verbose_name="Дата выбора")
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.user.username} лайкнул {self.recipe.title}"

    class Meta:
        verbose_name = 'Любимый рецепт'
        verbose_name_plural = 'Любимые рецепты'
