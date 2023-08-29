from django.contrib import admin

from .models import (CartRecipe, FavoriteRecipe, Ingredient, Recipe,
                     RecipeIngredient, Tag)


class IngredientInline(admin.TabularInline):
    model = RecipeIngredient
    fields = ("ingredient", "amount", "ingredient_display")
    list_filter = ("ingredient",)
    readonly_fields = ("ingredient_display",)

    def ingredient_display(self, instance):
        return f"({instance.ingredient.measurement_unit})"

    ingredient_display.short_description = "Measurement unit"


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "author", "in_favorites_times")
    list_display_links = ("name",)
    search_fields = ("name",)
    list_filter = ("author", "name", "tags")
    empty_value_display = "None"
    inlines = [
        IngredientInline,
    ]

    def in_favorites_times(self, obj):
        return f"{obj.Users.all().count()} users like this"


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "measurement_unit")
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "None"


class TagAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "color", "slug")
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "None"


class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "recipe")
    search_fields = ("recipe",)
    list_filter = ("recipe",)
    empty_value_display = "None"


class CartRecipeAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "recipe")
    search_fields = ("recipe",)
    list_filter = ("recipe",)
    empty_value_display = "None"


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(FavoriteRecipe, FavoriteRecipeAdmin)
admin.site.register(CartRecipe, CartRecipeAdmin)
