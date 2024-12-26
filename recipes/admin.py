from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from recipes.export import RecipeResource
from .models import Category, Ingredient, Recipe, RecIng, Step


class RecIngInline(admin.TabularInline):
    """Встраиваемое представление админки для модели RecIng"""
    model = RecIng
    extra = 1  # Число пустых форм, которые будут отображаться для добавления ингредиентов


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Интерфейс админки для модели Ingredient"""
    search_fields = ('name',)  # Поиск по названию ингредиента


class StepInline(admin.TabularInline):
    """Встраиваемое представление админки для модели Step."""
    model = Step
    extra = 1  # Кол-во доп. пустых форм, которые будут отображаться для добавления шагов.
    fields = ('step_number', 'description', 'photo')  # Указываем, какие поля отображать в инлайне.
    ordering = ('step_number',)  # Сортировать шаги по номеру шага.


@admin.register(Recipe)
class RecipeAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    """Админка для модели Рецепт"""
    inlines = [RecIngInline, StepInline]  # Отображение ингредиентов и шагов внутри формы рецепта.
    list_display = ('title', 'category', 'author', 'rating', 'status') #Поля для отображения
    list_filter = ('status', 'category',)  # Фильтрация по статусу и категории
    date_hierarchy = 'publish'
    search_fields = ('title', 'author__username')  # Поиск по заголовку и автору
    raw_id_fields = ('author',)
    resource_class = RecipeResource


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка для модели Категория"""
    search_fields = ('category_name',)  # Поиск по полям
