from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipes.views.category_view_set import CategoryModelViewSet
from recipes.views.filter_by_category import RecipeByCategoryView
from recipes.views.ingredient_view_set import IngredientModelViewSet
from recipes.views.recing_view_set import RecIngModelViewSet
from recipes.views.recipe_view_set import RecipeViewSet
from recipes.views import views

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipe-model')
router.register(r'recing', RecIngModelViewSet, basename='recipe-inredients')
router.register(r'ingredient', IngredientModelViewSet, basename='inredients')
router.register(r'category', CategoryModelViewSet, basename='category')

app_name = 'recipes'
urlpatterns = [
    path('api/', include(router.urls)),
    path('recipes/category/<int:category>/',
         RecipeByCategoryView.as_view(), name='recipe-category'),
    path('cookbook/', views.cookbook, name='cookbook'),
    path('search/', views.search_recipes, name='search'),
    path('recipe/<int:id>/', views.recipe_detail, name='recipe_detail'),
    # path('category/<int:id>/', views.category_recipes, name='category_recipes'),
]
