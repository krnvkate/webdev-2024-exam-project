from django.urls import path, include
from recipes.views.view_sets import RecipeViewSet
from rest_framework.routers import DefaultRouter
from recipes.views.filter_by_category import RecipeByCategoryView

router = DefaultRouter()
router.register(r'recipe-viewset', RecipeViewSet, basename='recipe-viewset')

urlpatterns = [
    path('', include(router.urls)),
    path('category/<int:category>/', RecipeByCategoryView.as_view(), name='recipe-category'),
]

