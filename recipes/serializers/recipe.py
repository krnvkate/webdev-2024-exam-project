from rest_framework import serializers
from recipes.models import Recipe
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from datetime import timedelta


class RecipeSerializer(serializers.ModelSerializer):
    ingredients_count = serializers.SerializerMethodField()
    steps_count = serializers.SerializerMethodField()
    publish = serializers.DateField(format='%d.%m.%Y')

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'author', 'category', 'ingredients_count', 'steps_count', 'main_photo', 'servings', 'calories', 'cook_time', 'rating', 'publish', 'status', 'notes']

    def get_ingredients_count(self, obj):
        return obj.ingredients.count()

    def get_steps_count(self, obj):
        return obj.steps.count()

    def validate_title(self, value):
        """ Проверка уникальности названия рецепта."""
        # Получаем ID текущего объекта
        recipe_id = self.instance.id if self.instance else None

        # Проверяем уникальность названия, исключая текущий объект
        if Recipe.objects.filter(title=value).exclude(id=recipe_id).exists():
            raise ValidationError("Рецепт с таким названием уже существует.")
        return value

    def validate_cook_time(self, value):
        """Проверка, что время приготовления не равно 00:00:00."""
        if value == timedelta(0):
            raise ValidationError("Время приготовления не может быть 00:00:00.")
        return value