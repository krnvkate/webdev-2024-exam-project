from rest_framework import serializers
from recipes.models import RecIng


class RecIngSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecIng
        fields = '__all__'

    def validate(self, data):
        recipe = data.get('recipe')

        if recipe is not None:
            ingredients_count = RecIng.objects.filter(recipe=recipe).count()
            if ingredients_count >= 20:
                raise serializers.ValidationError("Количество ингредиентов для одного рецепта не может превышать 20.")

        return data
