from rest_framework import viewsets
from recipes.models import Ingredient
from recipes.serializers.ingredient import IngredientSerializer
from rest_framework.filters import SearchFilter

class IngredientModelViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']
