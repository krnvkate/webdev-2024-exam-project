import os
from django.conf import settings
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from django.http import HttpResponse
import urllib.parse

# Регистрируем шрифт
FONT_PATH = os.path.join(settings.BASE_DIR, 'staticfiles', 'fonts', 'DejaVuSerif.ttf')
pdfmetrics.registerFont(TTFont('DejaVuSerif', FONT_PATH))


def generate_recipe_pdf(recipe):
    # Создаем объект HttpResponse с правильным PDF MIME-типом
    response = HttpResponse(content_type='application/pdf')
    # Кодируем название файла для безопасности
    safe_filename = urllib.parse.quote(f"{recipe.title}.pdf")
    response['Content-Disposition'] = f'attachment; filename="{safe_filename}"'

    # Создаем PDF документ
    doc = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    # Контейнер для элементов PDF
    elements = []

    # Определяем стили
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='CustomTitle',
        fontName='DejaVuSerif',
        fontSize=16,
        spaceAfter=30,
        alignment=1
    ))
    styles.add(ParagraphStyle(
        name='CustomBody',
        fontName='DejaVuSerif',
        fontSize=12,
        spaceAfter=12
    ))

    # Добавляем заголовок
    elements.append(Paragraph(recipe.title, styles['CustomTitle']))
    elements.append(Spacer(1, 12))

    # Основная информация
    elements.append(Paragraph(f"Категория: {recipe.category}", styles['CustomBody']))
    elements.append(Paragraph(f"Время приготовления: {recipe.cook_time}", styles['CustomBody']))
    elements.append(Paragraph(f"Порций: {recipe.servings}", styles['CustomBody']))
    elements.append(Paragraph(f"Калорийность: {recipe.calories} ккал", styles['CustomBody']))
    elements.append(Spacer(1, 12))

    # Ингредиенты
    elements.append(Paragraph("Ингредиенты:", styles['CustomBody']))
    ingredients_data = []
    for rec_ing in recipe.recing_set.all():
        ingredients_data.append([
            f"• {rec_ing.ingredient.name}",
            f"{rec_ing.quantity} {rec_ing.unit}"
        ])

    if ingredients_data:
        ing_table = Table(ingredients_data, colWidths=[300, 200])
        ing_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'DejaVuSerif'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
        ]))
        elements.append(ing_table)

    elements.append(Spacer(1, 12))

    # Шаги приготовления
    elements.append(Paragraph("Способ приготовления:", styles['CustomBody']))
    for step in recipe.steps.all():
        elements.append(Paragraph(
            f"{step.step_number}. {step.description}",
            styles['CustomBody']
        ))

    # Создаем PDF
    doc.build(elements)
    return response
