from django.urls import path, include
from recipes.views.recipe_view_set import RecipeViewSet
from recipes.views.recing_view_set import RecIngModelViewSet
from rest_framework.routers import DefaultRouter
from recipes.views.filter_by_category import RecipeByCategoryView
from recipes.views.ingredient_view_set import IngredientModelViewSet
from recipes.views.category_view_set import CategoryModelViewSet



router = DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipe-model')
router.register(r'recing', RecIngModelViewSet, basename='recipe-inredients')
router.register(r'ingredient', IngredientModelViewSet, basename='inredients')
router.register(r'category', CategoryModelViewSet, basename='category')



urlpatterns = [
    path('', include(router.urls)),
    path('recipes/category/<int:category>/', RecipeByCategoryView.as_view(), name='recipe-category'),
]


