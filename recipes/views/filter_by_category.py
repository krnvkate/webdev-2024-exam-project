from rest_framework import generics
from recipes.models import Recipe
from recipes.serializers.recipe import RecipeSerializer

class RecipeByCategoryView(generics.ListAPIView):
    serializer_class = RecipeSerializer

    def get_queryset(self):
        # Извлекаем category из URL
        category_id = self.kwargs.get('category')

        # Фильтруем рецепты по категории
        return Recipe.objects.filter(category_id=category_id)


