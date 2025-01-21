from django.shortcuts import render
from django.db.models import Count, Avg, Q
from recipes.models import Recipe, Category, Ingredient
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from recipes.models import Recipe
from .forms import RecipeForm


def cookbook(request):
    # Получаем популярные рецепты (топ по рейтингу)
    popular_recipes = Recipe.published.filter(rating__gte=4.0).order_by('-rating')[:5]

    # Получаем новые рецепты
    new_recipes = Recipe.published.order_by('-publish')[:3]

    # Получаем категории с подсчетом рецептов
    categories = Category.objects.annotate(
        recipe_count=Count('recipes')
    ).order_by('-recipe_count')[:8]

    # Статистика
    stats = {
        'total_recipes': Recipe.published.count(),
        'avg_calories': Recipe.published.aggregate(Avg('calories'))['calories__avg'],
        'total_categories': Category.objects.count(),
    }

    # Поиск
    search_query = request.GET.get('search', '')
    if search_query:
        search_results = Recipe.published.filter(
            Q(title__icontains=search_query) |
            Q(ingredients__name__icontains=search_query)
        ).distinct()
        # Пагинация результатов поиска
        paginator = Paginator(search_results, 6)
        page_number = request.GET.get('page', 1)
        try:
            search_results = paginator.page(page_number)
        except PageNotAnInteger:
            # Если page_number не целое число, то выдать первую страницу
            search_results = paginator.page(1)
        except EmptyPage:
            # Если page_number находится вне диапазона, то выдать последнюю страницу результатов
            search_results = paginator.page(paginator.num_pages)
    else:
        search_results = None

    # Фильтрация по категории
    category_id = request.GET.get('category')
    if category_id:
        filtered_recipes = Recipe.published.filter(category_id=category_id)
    else:
        filtered_recipes = None

    # Получение быстрых рецептов (менее 30 минут) с куриными яйцами
    quick_recipes = Recipe.published.filter(
        cook_time__lte='00:30:00'
    ).filter(ingredients__name='яйцо').order_by('cook_time')[:4]

    context = {
        'popular_recipes': popular_recipes,
        'new_recipes': new_recipes,
        'categories': categories,
        'stats': stats,
        'search_results': search_results,
        'search_query': search_query,
        'filtered_recipes': filtered_recipes,
        'quick_recipes': quick_recipes,
    }

    return render(request, 'recipes_main.html', context)


def search_recipes(request):
    query = request.GET.get('query', '')
    results = Recipe.published.filter(
        Q(title__icontains=query) |
        Q(ingredients__name__icontains=query)
    ).distinct()

    paginator = Paginator(results, 6)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'search_results.html', {
        'page_obj': page_obj,
        'query': query
    })


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipe_detail.html', {'recipe': recipe})


@login_required
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, author=request.user)
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            recipe = form.save()
            messages.success(request, 'Рецепт успешно обновлен')
            return redirect('recipes:recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipe_form.html', {'form': form})


@login_required
def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, author=request.user)
    if request.method == "POST":
        recipe.delete()
        messages.success(request, 'Рецепт успешно удален')
        return redirect('recipes:cookbook')
    return redirect('recipes:recipe_detail', recipe_id=recipe_id)


@login_required
def recipe_new(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            messages.success(request, 'Рецепт успешно создан')
            return redirect('recipes:recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm()
    return render(request, 'recipe_form.html', {'form': form})


def category_recipes(request, id):
    category = get_object_or_404(Category, id=id)
    recipes = Recipe.published.filter(category=category)

    # Пагинация
    paginator = Paginator(recipes, 9)
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


