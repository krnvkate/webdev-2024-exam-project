from rest_framework import viewsets, status
from recipes.models import Recipe
from recipes.seriallizers.recipe import RecipeSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class RecipeViewSet(viewsets.ViewSet):
    def list (self, request):
        queryset = Recipe.objects.all()
        serializer = RecipeSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        serializer = RecipeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Recipe.objects.all()
        recipe = get_object_or_404(queryset, pk=pk)
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data)

    def update(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = RecipeSerializer(recipe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)