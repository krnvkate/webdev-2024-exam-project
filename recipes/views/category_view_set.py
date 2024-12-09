from rest_framework import viewsets
from recipes.models import Category
from recipes.serializers.category import CategorySerializer
from rest_framework.filters import SearchFilter

class CategoryModelViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter]
    search_fields = ['category_name']