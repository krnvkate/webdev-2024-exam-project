from rest_framework import viewsets
from recipes.models import Recipe
from recipes.serializers.recipe import RecipeSerializer

# пример с ModelViewSet
class RecipeModelViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
