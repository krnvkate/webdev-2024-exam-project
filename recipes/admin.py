from django.contrib import admin

from .models import Category, Ingredient, Recipe, RecIng, Step
class RecIngInline(admin.TabularInline):
    model = RecIng
    extra = 1  # Число пустых форм, которые будут отображаться для добавления ингредиентов

class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecIngInline,)  # Ингредиенты как инлайн формы

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Отображение списка ингредиентов

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecIngInline]  # Отображение ингредиентов внутри формы рецепта
    list_display = ('title', 'category', 'servings', 'cook_time', 'rating', 'status')  # Поля для отображения в списке рецептов
admin.site.register(Category)
admin.site.register(Step)
