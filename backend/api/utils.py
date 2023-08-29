import io

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def prepare_shopping_list(ingredients):
    """Transforms queryset of ingredients to a BytesIO object
    with the shopping list.
    """
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    pdfmetrics.registerFont(
        TTFont("FreeSans", "foodgram_static/freesans.ttf", "UTF-8")
    )
    p.setFont("FreeSans", 24)
    p.setFillColorRGB(0, 0, 255)
    p.drawString(50, 770, "ИНГРЕДИЕНТЫ для покупки")
    p.setFillColorRGB(0, 0, 0)
    p.setFont("FreeSans", 14)
    p.drawString(50, 750, "(на основе рецептов в вашей корзине)")
    p.line(10, 725, 550, 725)
    pos_y = 700
    for num, ingredient in enumerate(ingredients, start=1):
        p.drawString(
            50,
            pos_y,
            (
                f"{num}) {ingredient['ingredient__name']} "
                f"{ingredient['total_amount']} "
                f"{ingredient['ingredient__measurement_unit']}"
            ),
        )
        pos_y -= 25
    p.line(10, pos_y, 550, pos_y)
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer
