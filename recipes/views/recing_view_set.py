from rest_framework import viewsets
from recipes.models import RecIng
from recipes.serializers.recing import RecIngSerializer

class RecIngModelViewSet(viewsets.ModelViewSet):
    queryset = RecIng.objects.all()
    serializer_class = RecIngSerializer
