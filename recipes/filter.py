from django_filters.rest_framework import FilterSet, CharFilter
from recipes.models import Recipe


class RecipeFilter(FilterSet):
    title_name = CharFilter(field_name="title", lookup_expr='icontains')

    class Meta:
        model = Recipe
        fields = ['title']
