from django_filters.rest_framework import FilterSet, CharFilter, DurationFilter, NumberFilter

from recipes.models import Recipe


class RecipeFilter(FilterSet):
    """Фильтры для рецептов"""
    title_name = CharFilter(field_name='title', lookup_expr='icontains')
    ingredients = CharFilter(field_name='ingredients__name', lookup_expr='icontains')
    cook_time_min = \
        DurationFilter(field_name='cook_time', lookup_expr='gte', label='Минимальное время готовки')
    cook_time_max = \
        DurationFilter(field_name='cook_time', lookup_expr='lte', label='Максимальное время готовки')
    calories_min = \
        NumberFilter(field_name='calories', lookup_expr='gte', label='Минимальная калорийность')
    calories_max = \
        NumberFilter(field_name='calories', lookup_expr='lte', label='Максимальная калорийность')

    class Meta:
        model = Recipe
        fields = ['cook_time_min', 'cook_time_max', 'calories_min', 'calories_max']
