from django.contrib import admin

from .models import Recipe, Ingredient, Tag, RecipeIngredient


class IngredientInline(admin.TabularInline):
    model = RecipeIngredient
    fields = ('ingredient', 'amount', 'ingredient_display')
    readonly_fields = ('ingredient_display',)

    def ingredient_display(self, instance):
        return f"({instance.ingredient.measurement_unit})"

    ingredient_display.short_description = 'Measurement unit'


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author', 'text', 'cooking_time')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-empty-'
    inlines = [ 
        IngredientInline,
    ]


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-empty-'


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-empty-'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
