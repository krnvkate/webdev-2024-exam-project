from django import forms
from recipes.models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'category', 'servings', 'cook_time', 'calories',
                'main_photo', 'notes', 'ingredients']
        exclude = ['author']
        widgets = {
            'cook_time': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'title': 'Название рецепта',
        }
        help_texts = {
            'description': 'Введите описание рецепта',
        }
        error_messages = {
            'title': {
                'required': 'Это поле обязательно.',
            },
        }

    class Media:
        css = {
            'all': ('css/recipe_form.css',)
        }

