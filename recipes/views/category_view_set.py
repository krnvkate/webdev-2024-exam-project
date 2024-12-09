from rest_framework import viewsets
from recipes.models import Category
from recipes.serializers.category import CategorySerializer

class CategoryModelViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer