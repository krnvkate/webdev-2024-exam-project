from django.db.models import Count, Avg, Q
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Avg, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from recipes.models import Category
from recipes.models import Recipe
from .forms import RecipeForm, RecipeIngredientFormSet, StepFormSet


def cookbook(request):
    # Получаем дату месяц назад
    month_ago = timezone.now() - timedelta(days=30)

    # Получаем популярные рецепты за месяц
    popular_recipes = Recipe.published.select_related('author', 'category').filter(
        publish__gte=month_ago).filter(rating__gte=4.5).order_by('-rating')[:5]

    # Получаем новые рецепты
    new_recipes = Recipe.published.select_related('author', 'category').order_by('-publish')[:3]

    # Получаем категории с подсчетом рецептов
    categories = Category.objects.annotate(
        recipe_count=Count('recipes', filter=Q(recipes__status=Recipe.Status.PUBLISHED))
    ).order_by('-recipe_count')

    # Статистика
    stats = {
        'total_recipes': Recipe.published.count(),
        'avg_calories': Recipe.published.aggregate(Avg('calories'))['calories__avg'],
        'total_categories': Category.objects.count(),
    }

    # Поиск - редирект на отдельную страницу поиска
    search_query = request.GET.get('search', '')
    if search_query:
        return redirect('recipes:search') + '?query=' + search_query

    context = {
        'popular_recipes': popular_recipes,
        'new_recipes': new_recipes,
        'categories': categories,
        'stats': stats,
    }

    return render(request, 'recipes_main.html', context)


def search_recipes(request):
    query = request.GET.get('query', '')
    search_criteria = []
    if query:
        title_results = Recipe.published.select_related('author', 'category').filter(title__contains=query)            # Поиск по названию
        ingredient_results = Recipe.published.select_related('author', 'category').filter(ingredients__name__icontains=query)  # Поиск по ингредиентам
        results = (title_results | ingredient_results).distinct()                     # Объединяем результаты
        if title_results.exists():               # Определяем критерии поиска
            search_criteria.append('названию')
        if ingredient_results.exists():
            search_criteria.append('ингредиентам')
    else:
        results = Recipe.published.none()
    paginator = Paginator(results, 3)
    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'search_results.html', {
        'page_obj': page_obj,
        'query': query,
        'search_criteria': search_criteria
    })


def category_recipes(request, id):
    category = get_object_or_404(Category, id=id)
    recipes_list = Recipe.published.select_related('author', 'category').filter(category=category)

    # Пагинация
    paginator = Paginator(recipes_list, 3)
    page_number = request.GET.get('page')
    try:
        recipes = paginator.page(page_number)
    except PageNotAnInteger:
        recipes = paginator.page(1)
    except EmptyPage:
        recipes = paginator.page(paginator.num_pages)

    return render(request, 'category_recipes.html', {
        'category': category,
        'recipes': recipes
    })


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe.objects.select_related('author', 'category').prefetch_related(
            'ingredients',
            'steps',
            'recing_set'
        ), id=recipe_id)
    return render(request, 'recipe_detail.html', {'recipe': recipe})


@login_required
def recipe_new(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        ingredient_formset = RecipeIngredientFormSet(request.POST, prefix='ingredients')
        step_formset = StepFormSet(request.POST, request.FILES, prefix='steps')

        if form.is_valid() and ingredient_formset.is_valid() and step_formset.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            ingredient_formset.instance = recipe
            ingredient_formset.save()

            step_formset.instance = recipe
            step_formset.save()

            messages.success(request, 'Рецепт успешно создан')
            return redirect('recipes:recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm()
        ingredient_formset = RecipeIngredientFormSet(prefix='ingredients')
        step_formset = StepFormSet(prefix='steps')

    return render(request, 'recipe_form.html', {
        'form': form,
        'ingredient_formset': ingredient_formset,
        'step_formset': step_formset
    })


@login_required
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe.objects.select_related('author').prefetch_related('recing_set', 'steps'), id=recipe_id, author=request.user)
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        ingredient_formset = RecipeIngredientFormSet(request.POST, prefix='ingredients', instance=recipe)
        step_formset = StepFormSet(request.POST, request.FILES, prefix='steps', instance=recipe)

        if form.is_valid() and ingredient_formset.is_valid() and step_formset.is_valid():
            recipe = form.save()
            ingredient_formset.save()
            step_formset.save()

            messages.success(request, 'Рецепт успешно обновлен')
            return redirect('recipes:recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)
        ingredient_formset = RecipeIngredientFormSet(prefix='ingredients', instance=recipe)
        step_formset = StepFormSet(prefix='steps', instance=recipe)

    return render(request, 'recipe_form.html', {
        'form': form,
        'ingredient_formset': ingredient_formset,
        'step_formset': step_formset
    })


@login_required
def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, author=request.user)
    if request.method == "POST":
        recipe.delete()
        messages.success(request, 'Рецепт успешно удален')
        return redirect('recipes:cookbook')
    return redirect('recipes:recipe_detail', recipe_id=recipe_id)
