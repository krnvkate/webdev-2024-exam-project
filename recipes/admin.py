from django.contrib import admin
from django.utils.html import format_html
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
    list_display = ('title', 'category', 'author', 'rating_colored', 'status') #Поля для отображения
    list_filter = ('status', 'category', 'rating')  # Фильтрация по статусу и категории, рейтингу
    date_hierarchy = 'publish'
    search_fields = ('title', 'author__username')  # Поиск по заголовку и автору
    raw_id_fields = ('author',)
    list_display_links = ('title', 'author')
    resource_class = RecipeResource
    actions = ['mark_as_published']

    @admin.display(description='Рейтинг', ordering='rating')
    def rating_colored(self, obj):
        if obj.rating >= 4.5:
            color = 'green'
        elif obj.rating >= 3.0:
            color = 'orange'
        else:
            color = 'red'
        return format_html('<span style="color: {};">{}</span>', color, obj.rating)

    def mark_as_published(self, request, queryset):
        queryset.update(status=Recipe.Status.PUBLISHED)

    mark_as_published.short_description = "Отметить как опубликованные"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка для модели Категория"""
    search_fields = ('category_name',)  # Поиск по полям
