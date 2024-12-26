from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from recipes.models import Category
from recipes.serializers.category import CategorySerializer


class CategoryModelViewSet(viewsets.ModelViewSet):
    """Вьюшка CRUD для модели Категория"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter]
    search_fields = ['category_name']
