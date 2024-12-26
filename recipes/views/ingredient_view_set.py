from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from recipes.models import Ingredient
from recipes.serializers.ingredient import IngredientSerializer


class IngredientModelViewSet(viewsets.ModelViewSet):
    """Вьюшка CRUD для модели Ингредиент"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']
