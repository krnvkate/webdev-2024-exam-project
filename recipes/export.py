from import_export.resources import ModelResource
from recipes.models import Recipe


class RecipeResource(ModelResource):
    """Экспорт данных из админки в excel"""
    class Meta:
        """Данные, доступные для экспорта"""
        model = Recipe
        fields = ('id', 'title', 'author', 'category', 'cook_time',
                  'rating', 'publish', 'status', 'ingredients')

    def get_export_queryset(self, request):
        """Получаем базовый queryset из ModelAdmin"""
        queryset = super().get_queryset(request)
        return queryset.filter(rating__gt=4.0)

    def dehydrate_author(self, recipe: Recipe) -> str:
        """Возвращаем никнейм автора вместо ID"""
        return str(recipe.author)

    def dehydrate_ingredients(self, recipe: Recipe) -> str:
        """Преобразуем список ингредиентов в строку, разделённую запятыми"""
        return ', '.join(str(ingredient) for ingredient in recipe.ingredients.all())

    def get_category_type(self, recipe: Recipe) -> str:
        """Преобразуем поле category в формат "Категория: {тип}" """
        return f"Категория: {recipe.category.category_name}" \
            if recipe.category else "Категория: Не указана"

    def dehydrate_category(self, recipe: Recipe) -> str:
        """Используем get_category_type для форматирования значения категории"""
        return self.get_category_type(recipe)
