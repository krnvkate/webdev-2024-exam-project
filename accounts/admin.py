"""Настройка админки для приложения accounts"""
from django.contrib import admin

from .models import Profile, FavoriteRecipe


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_email', 'get_full_name', 'country', 'city', 'is_staff')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    list_filter = ('country', 'city', 'user__is_staff', 'user__is_superuser')

    @admin.display(description='Email')
    def get_email(self, obj):
        return obj.user.email

    @admin.display(description='Полное имя')
    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    @admin.display(description='Статус персонала')
    def is_staff(self, obj):
        return obj.user.is_staff

    is_staff.boolean = True


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'fav_date')
    search_fields = ('user__username', 'recipe__title')
    date_hierarchy = 'fav_date'
    readonly_fields = ('fav_date',)
