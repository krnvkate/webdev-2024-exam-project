from rest_framework import viewsets
from recipes.models import Ingredient
from recipes.serializers.ingredient import IngredientSerializer

class IngredientModelViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer