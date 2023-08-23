from django.contrib import admin
from users.models import Follow, User

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
    list_display = ("pk", "name", "author")
    list_display_links = ("name",)
    search_fields = ("name",)
    list_filter = ("author", "name", "tags")
    empty_value_display = "None"
    inlines = [
        IngredientInline,
    ]


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


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "username",
        "first_name",
        "last_name",
        "email",
        "role",
    )
    list_display_links = ("username",)
    list_filter = ("email", "first_name")


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


class FollowAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "author")
    search_fields = ("author",)
    list_filter = ("author",)
    empty_value_display = "None"


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(FavoriteRecipe, FavoriteRecipeAdmin)
admin.site.register(CartRecipe, CartRecipeAdmin)
admin.site.register(Follow, FollowAdmin)
