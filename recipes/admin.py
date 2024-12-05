from django.contrib import admin

from .models import Category, Ingredient, Recipe, RecIng, Step
class RecIngInline(admin.TabularInline):
    model = RecIng
    extra = 1  # Число пустых форм, которые будут отображаться для добавления ингредиентов

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('name',)  # Поиск по названию ингредиента

class StepInline(admin.TabularInline):
    model = Step
    extra = 1  # Количество дополнительных пустых форм, которые будут отображаться для добавления шагов.
    fields = ('step_number', 'description', 'photo')  # Указываем, какие поля отображать в инлайне.
    ordering = ('step_number',)  # Сортировать шаги по номеру шага.

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecIngInline, StepInline]  # Отображение ингредиентов и шагов внутри формы рецепта.
    list_display = ('title', 'category', 'author', 'rating', 'status')  # Поля для отображения в списке рецептов
    list_filter = ('status', 'category',)  # Фильтрация по статусу и категории
    date_hierarchy = 'publish'
    search_fields = ('title', 'author__username')  # Поиск по заголовку и автору
    raw_id_fields = ('author',)


# @admin.register(Step)
# class StepAdmin(admin.ModelAdmin):
#     list_display = ('recipe', 'step_number')  # Показать рецепт и номер шага
#     ordering = ('step_number',)  # Сортировка по номеру шага
#     search_fields = ('recipe__title',)  # Поиск по названию рецепта


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('category_name',)  # Поиск по полям
    #list_filter = ('category_name',)  # Фильтрация по имени категории