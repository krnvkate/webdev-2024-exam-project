from rest_framework import serializers
from recipes.models import Recipe
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username']

class RecipeSerializer(serializers.ModelSerializer):
    ingredients_count = serializers.SerializerMethodField()
    steps_count = serializers.SerializerMethodField()
    author = UserSerializer()
    publish = serializers.DateTimeField(format='%d.%m.%Y')

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'author', 'category', 'cook_time', 'rating', 'publish', 'status', 'ingredients_count', 'steps_count']

    def get_ingredients_count(self, obj):
        return obj.ingredients.count()

    def get_steps_count(self, obj):
        return obj.steps.count()

    def validate_title(self, value):
        """ Проверка уникальности названия рецепта."""
        if Recipe.objects.filter(title=value).exists():
            raise ValidationError("Рецепт с таким названием уже существует.")
        return value