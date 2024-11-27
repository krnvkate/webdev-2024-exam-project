from django.conf import settings
from django.db import models
from recipes.models import Recipe

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    avatar = models.ImageField(upload_to='users_avatar', blank=True, verbose_name="Фото профиля")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    country = models.CharField(max_length=50, null=True, blank=True, verbose_name="Страна")
    city = models.CharField(max_length=50, null=True, blank=True, verbose_name="Город")
    info = models.TextField(null=True, blank=True, verbose_name="О себе")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

class FavoriteRecipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='like_recipe', verbose_name="Пользователь")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='users_like', verbose_name="Понравившийся рецепт")
    fav_date = models.DateField(verbose_name="Дата выбора")

    def __str__(self):
        return f"{self.user.username} лайкнул {self.recipe.title}"

    class Meta:
        verbose_name = 'Любимый рецепт'
        verbose_name_plural = 'Любимые рецепты'