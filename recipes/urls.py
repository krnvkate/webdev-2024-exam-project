from django.urls import path, include
from recipes.views.recipe_view_set import RecipeViewSet
from recipes.views.recing_view_set import RecIngModelViewSet
from rest_framework.routers import DefaultRouter
from recipes.views.filter_by_category import RecipeByCategoryView
from recipes.views.filter_by_cook_time import RecipeByCookTimeView

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipe-model')
router.register(r'recing', RecIngModelViewSet, basename='recipe-inredients')

urlpatterns = [
    path('api/', include(router.urls)),
    path('category/<int:category>/', RecipeByCategoryView.as_view(), name='recipe-category'),
    path('recipes/title/', RecipeByCookTimeView.as_view(), name='filtered-recipes'),
]


