from rest_framework import generics
from recipes.models import Recipe
from recipes.serializers.recipe import RecipeSerializer

class RecipeByCookTimeView(generics.ListAPIView):
    serializer_class = RecipeSerializer

    def get_queryset(self):
        # Получаем все рецепты по умолчанию
        queryset = Recipe.objects.all()

        # Получаем GET-параметр 'title'
        title = self.request.query_params.get('title', None)

        # Если передан параметр 'title', фильтруем по названию
        if title:
            queryset = queryset.filter(title__icontains=title)  # Фильтрация по частичному совпадению

        return queryset