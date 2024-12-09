from rest_framework import viewsets, status
from recipes.models import Recipe
from django.db.models import Q
from accounts.models import FavoriteRecipe
from recipes.serializers.recipe import RecipeSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django.db.models import Count
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from recipes.filter import RecipeFilter

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['title']
    filterset_class = RecipeFilter


    @action(methods=['get', 'post'], detail=True)
    def add_note_good_food(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        note = 'Полезная еда'
        recipe.notes = note
        recipe.save()
        return Response({'status': 'Note added'})

    @action(methods=['get', 'post'], detail=True)
    def add_note_bad_food(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        note = 'Вредная еда'
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

    @action(methods=["GET"], detail=False)
    def get_soup_health(self, request):
        """
        Категория "Супы" И (ингредиенты "курица" ИЛИ "красная рыба")
        И калорийность НЕ больше 500
        """
        recipes = Recipe.objects.filter(
            Q(category__category_name='Супы') &
            (Q(ingredients__name='курица') | Q(ingredients__name='красная рыба')) &
            ~Q(calories__gt=500)
        ).distinct()

        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

    @action(methods=["GET"], detail=False)
    def get_choco_or_20min(self, request):
        """
        (содержит "шоколад" И (не категория "Десерты"))
        ИЛИ (время приготовления меньше 20 минут)
        """
        recipes = Recipe.objects.filter(
            (Q(ingredients__name='шоколад') &
            ~Q(category__category_name='Десерты')) |
            Q(cook_time__lt=timezone.timedelta(minutes=20))
        ).distinct()

        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

