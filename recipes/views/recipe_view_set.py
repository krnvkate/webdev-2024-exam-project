from django.core.cache import cache
from django.db.models import Count
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from accounts.models import FavoriteRecipe
from recipes.filter import RecipeFilter
from recipes.models import Recipe
from recipes.serializers.recipe import RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюшка CRUD для модели Рецепт"""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['notes']
    filterset_class = RecipeFilter

    def get_recipe(self, recipe_id):
        cache_key = f"recipe_{recipe_id}"
        recipe = cache.get(cache_key)

        if recipe is None:
            print("Cache miss - getting from database")
            recipe = get_object_or_404(Recipe, pk=recipe_id)
            cache.set(cache_key, recipe, timeout=60 * 15)
        else:
            print("Cache hit - getting from Redis")

        return recipe

    @action(methods=['get', 'post'], detail=True)
    def add_note_good_food(self, request, pk=None):
        """Функция добавления заметки с текстом: "Полезная еда" к рецепту"""
        recipe = get_object_or_404(Recipe, pk=pk)
        note = 'Полезная еда'
        recipe.notes = note
        recipe.save()
        return Response({'status': 'Note added'})

    @action(methods=['get', 'post'], detail=True)
    def add_note_bad_food(self, request, pk=None):
        """Функция добавления заметки с текстом: "Вредная еда" к рецепту"""
        recipe = get_object_or_404(Recipe, pk=pk)
        note = 'Вредная еда'
        recipe.notes = note
        recipe.save()
        return Response({'status': 'Note added'})

    @action(methods=['get'], detail=False)
    def popular(self, request):
        """Получение рецептов,имеющих лайки, и сортировка их"""
        popular_recipes = Recipe.objects.annotate(like_count=Count('users_like'))\
            .filter(like_count__gt=0).order_by('-like_count')

        serializer = RecipeSerializer(popular_recipes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # permission_classes = [IsAuthenticated]
    @action(methods=['post'], detail=True)
    def add_to_favorites(self, request, pk=None):
        """Функция добавления рецепта в избранное"""
        # Получаем рецепт по pk (идентификатору)
        recipe = get_object_or_404(Recipe, pk=pk)

        # Проверяем, существует ли уже запись о любимом рецепте для этого пользователя
        if FavoriteRecipe.objects.filter(user=request.user, recipe=recipe).exists():
            return Response({'detail': 'Рецепт уже в ваших избранных.'},
                            status=status.HTTP_400_BAD_REQUEST)

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
