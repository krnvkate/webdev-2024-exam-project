from django.shortcuts import render
from django.db.models import Count, Avg, Q
from recipes.models import Recipe, Category, Ingredient
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def cookbook(request):
    # Получаем популярные рецепты (топ по рейтингу)
    popular_recipes = Recipe.published.order_by('-rating')[:5]

    # Получаем новые рецепты
    new_recipes = Recipe.published.order_by('-publish')[:6]

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
        search_results = paginator.get_page(page_number)
    else:
        search_results = None

    # Фильтрация по категории
    category_id = request.GET.get('category')
    if category_id:
        filtered_recipes = Recipe.published.filter(category_id=category_id)
    else:
        filtered_recipes = None

    # Получение быстрых рецептов (менее 30 минут)
    quick_recipes = Recipe.published.filter(
        cook_time__lte='00:30:00'
    ).order_by('cook_time')[:4]

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


def recipe_detail(request,):
    recipe = get_object_or_404(Recipe, status=Recipe.Status.PUBLISHED)
    return render(request,
                  'recipe_detail.html',
                  {'recipe': recipe})

