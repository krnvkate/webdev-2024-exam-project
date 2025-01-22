from django import forms
from django.forms import inlineformset_factory
from recipes.models import Recipe, RecIng, Step


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'category', 'servings', 'cook_time', 'calories', 'main_photo', 'notes']
        exclude = ['author', 'status', 'rating']
        widgets = {
            'cook_time': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'title': 'Название рецепта',
            'category': 'Категория',
            'servings': 'Число порций',
            'cook_time': 'Время приготовления чч:мм',
            'calories': 'Калории',
            'main_photo': 'Основное фото',
            'notes': 'Комментарии',
        }
        help_texts = {
            'title': 'Введите название рецепта, которое будет видно всем.',
            'servings': 'Количество порций, на которое рассчитан рецепт.',
            'calories': 'Калории на одну порцию.',
        }
        error_messages = {
            'title': {
                'max_length': "Убедитесь, что название не превышает 200 символов.",
                'required': "Это поле обязательно для заполнения.",
            },
            'calories': {
                'error': "Калории не могут быть отрицательными.",
            },
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 3:
            raise forms.ValidationError("Название должно содержать минимум 3 символа")
        return title

    def clean(self):
        cleaned_data = super().clean()
        calories = cleaned_data.get('calories')
        if calories is not None and calories < 0:
            self.add_error('calories', "Калории не могут быть отрицательными.")
        return cleaned_data

    def save(self, commit=True):
        recipe = super().save(commit=False)
        if commit:
            recipe.save()
        return recipe


RecipeIngredientFormSet = inlineformset_factory(
    Recipe, RecIng,
    fields=('ingredient', 'quantity', 'unit'),
    extra=1,
    can_delete=True
)

StepFormSet = inlineformset_factory(
    Recipe, Step,
    fields=('step_number', 'description', 'photo'),
    extra=1,
    can_delete=True
)
