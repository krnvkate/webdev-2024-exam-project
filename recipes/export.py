from import_export.resources import ModelResource
from recipes.models import Recipe


class RecipeResource(ModelResource):
    class Meta:
        model = Recipe
        fields = ('id', 'title', 'author', 'category', 'cook_time', 'rating', 'publish', 'status', 'notes')

    def get_export_queryset(self, Recipe):
        # Возвращаем только рецепты с рейтингом выше 4
        return Recipe.get_export_queryset().filter(rating__gt=4)


    # # Преобразуйте список ингредиентов в строку,разделенную запятыми.
    # def dehydrate_ingredients:
    # # Преобразуйте поле category в формат "Кухня: {тип кухни}".
    # def get_category_type: