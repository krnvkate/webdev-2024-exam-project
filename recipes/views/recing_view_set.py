from rest_framework import viewsets
from recipes.models import RecIng
from recipes.serializers.recing import RecIngSerializer
from rest_framework.filters import SearchFilter


class RecIngModelViewSet(viewsets.ModelViewSet):
    """Вьюшка CRUD для модели Рецепт-ингредиент"""
    queryset = RecIng.objects.all()
    serializer_class = RecIngSerializer
    filter_backends = [SearchFilter]
    search_fields = ['unit']
