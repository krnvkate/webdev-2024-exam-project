"""Настройка админки для приложения accounts"""
from django.contrib import admin

from .models import Profile, FavoriteRecipe


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Представление модели Профиль в админке"""
    list_display = ('user', 'user__email', 'user__first_name', 'country', 'city', 'user__is_staff')
    search_fields = ('user__username','user__email', 'user__first_name', 'user__last_name')
    list_filter = ('country', 'city', 'user__is_staff', 'user__is_superuser', 'user__is_active')


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    """Представление модели Любимый рецепт в админке"""
    list_display = ('user', 'recipe', 'fav_date')  # Показать, кто лайкнул какой рецепт и когда
    search_fields = ('user__username', 'recipe__title')
    date_hierarchy = 'fav_date'
