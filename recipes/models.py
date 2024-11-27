from django.db import models
from django.conf import settings
from django.utils import timezone

class Category(models.Model):
    category_name = models.CharField(max_length=50, verbose_name="Категория", help_text="Введите название категории")
    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Ingredient(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название ингредиента')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

class Recipe(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DT', 'Удалён'
        CHECK = 'CK', 'На рассмотрении'
        PUBLISHED = 'PB', 'Опубликован'

    title = models.CharField(max_length=200, verbose_name='Название рецепта')
    servings = models.PositiveIntegerField(verbose_name='Число порций')
    cook_time = models.DurationField(verbose_name='Время приготовления')
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5,
                                         verbose_name='Рейтинг')
    main_photo = models.ImageField(upload_to='recipes/main_photos', verbose_name='Основное фото')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='recipes', verbose_name="Автор")
    calories = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2, verbose_name="Калории на одну порцию")
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='recipes', verbose_name="Категория")
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.CHECK, verbose_name="Статус")
    ingredients = models.ManyToManyField(Ingredient, through="RecIng", verbose_name="Ингредиент")
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-publish']  #Сортировка по дате загрузки, сначала новые
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

class RecIng(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="Рецепт")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name="Ингредиент")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Количество")
    unit_choices = [
        ('л', 'Литр'),
        ('мл', 'Миллилитр'),
        ('ст', 'Стакан'),
        ('ст. л', 'Столовая ложка'),
        ('ч. л', 'Чайная ложка'),
        ('шт', 'Штук'),
        ('гр', 'Грамм'),
        ('кг', 'Килограмм'),
    ]
    unit = models.CharField(max_length=5, choices=unit_choices, verbose_name="Единица измерения")

    def __str__(self):
        return f"{self.quantity} {self.unit} {self.ingredient.name} для {self.recipe.title}"

    class Meta:
        verbose_name = "Количество ингредиента"
        verbose_name_plural = "Количество ингредиентов"

class Step(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='steps',verbose_name="Рецепт")
    step_number = models.PositiveIntegerField(verbose_name="Номер шага")
    description = models.TextField(verbose_name="Описание шага")
    photo = models.ImageField(upload_to='recipes/steps/', blank=True, null=True, verbose_name="Фото к шагу")

    def __str__(self):
        return f"Шаг {self.step_number} для рецепта '{self.recipe.title}'"

    class Meta:
        ordering = ['step_number']  # Сортировка по номеру шага (по возрастанию)
        unique_together = ('recipe', 'step_number')  # Уникальность номера шага в рамках одного рецепта
        verbose_name = "Шаг"
        verbose_name_plural = "Шаги"