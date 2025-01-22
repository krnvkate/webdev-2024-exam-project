from django import template
from datetime import timedelta

register = template.Library()


@register.filter(name='format_duration')
def format_duration(value):
    if isinstance(value, str):
        try:
            # Преобразуем строку в timedelta
            hours, minutes, seconds = map(int, value.split(':'))
            value = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        except ValueError:
            return value

    total_minutes = int(value.total_seconds() / 60)
    hours = total_minutes // 60
    minutes = total_minutes % 60

    if hours > 0:
        if minutes > 0:
            return f"{hours} ч. {minutes} мин."
        else:
            return f"{hours} ч."
    return f"{minutes} мин."


@register.filter(name='plural_recipes')
def plural_recipes(number):
    last_digit = number % 10
    last_two_digits = number % 100

    if last_two_digits in range(11, 20):
        return f"{number} рецептов"
    elif last_digit == 1:
        return f"{number} рецепт"
    elif last_digit in range(2, 5):
        return f"{number} рецепта"
    else:
        return f"{number} рецептов"
