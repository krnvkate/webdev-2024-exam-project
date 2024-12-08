from rest_framework import viewsets, status
from recipes.models import Recipe
from accounts.models import FavoriteRecipe
from recipes.serializers.recipe import RecipeSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django.db.models import Count
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

# class RecipeViewSet(viewsets.ViewSet):
class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    # def list (self, request):
    #     queryset = Recipe.objects.all()
    #     serializer = RecipeSerializer(queryset, many=True)
    #     return Response(serializer.data)
    #
    # def create(self, request):
    #     data = request.data
    #     serializer = RecipeSerializer(data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def retrieve(self, request, pk=None):
    #     queryset = Recipe.objects.all()
    #     recipe = get_object_or_404(queryset, pk=pk)
    #     serializer = RecipeSerializer(recipe)
    #     return Response(serializer.data)
    #
    # def update(self, request, pk=None):
    #     recipe = get_object_or_404(Recipe, pk=pk)
    #     serializer = RecipeSerializer(recipe, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def destroy(self, request, pk=None):
    #     recipe = get_object_or_404(Recipe, pk=pk)
    #     recipe.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True)
    def add_note(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        note = request.data.get('notes', '')
        recipe.notes = note
        recipe.save()
        return Response({'status': 'Note added'})

    @action(methods=['get'], detail=False)
    def popular(self, request):
        # Получаем рецепты, которые имеют лайки, и сортируем их по количеству лайков
        popular_recipes = Recipe.objects.annotate(like_count=Count('users_like')).filter(like_count__gt=0).order_by(
            '-like_count')

        serializer = RecipeSerializer(popular_recipes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # permission_classes = [IsAuthenticated]
    @action(methods=['post'], detail=True)
    def add_to_favorites(self, request, pk=None):
        # Получаем рецепт по pk (идентификатору)
        recipe = get_object_or_404(Recipe, pk=pk)

        # Проверяем, существует ли уже запись о любимом рецепте для этого пользователя
        if FavoriteRecipe.objects.filter(user=request.user, recipe=recipe).exists():
            return Response({'detail': 'Этот рецепт уже в ваших избранных.'}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем запись о любимом рецепте
        favorite_recipe = FavoriteRecipe(user=request.user, recipe=recipe, fav_date=timezone.now())
        favorite_recipe.save()
        return Response({'detail': 'Рецепт добавлен в избранное!'}, status=status.HTTP_201_CREATED)