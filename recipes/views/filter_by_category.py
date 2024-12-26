from rest_framework import generics

from recipes.models import Recipe
from recipes.serializers.recipe import RecipeSerializer


class RecipeByCategoryView(generics.ListAPIView):
    """Фильтр по именованным аргументам в URL - по категории"""
    serializer_class = RecipeSerializer

    def get_queryset(self):
        """Функция для получения списка рецептов этой категории"""
        # Извлекаем category из URL
        category_id = self.kwargs.get('category')
        # Фильтруем рецепты по категории
        return Recipe.objects.filter(category_id=category_id)
