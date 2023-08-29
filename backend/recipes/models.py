from colorfield.fields import ColorField
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Tag(models.Model):
    """Tag db model class."""

    name = models.CharField(
        "Name",
        max_length=256,
        unique=True,
    )
    color = ColorField(default='#FF0000')
    slug = models.SlugField(
        "Slug",
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient db model class."""

    name = models.CharField("Name", max_length=256)
    measurement_unit = models.CharField("Measurement unit", max_length=10)

    class Meta:
        verbose_name = "Ingredient"
        verbose_name_plural = "Ingredients"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "measurement_unit"],
                name="ingredient_with_this_measure_already_exists",
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.measurement_unit})"


class Recipe(models.Model):
    """Recipe db model class."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="Recipes",
        verbose_name="Author",
    )
    name = models.CharField("Name", max_length=settings.LIMIT_RECIPE_NAME)
    text = models.TextField(
        "Text",
    )
    cooking_time = models.PositiveSmallIntegerField(
        "Cooking time",
        validators=(
            MinValueValidator(
                1, message='Time of cooking should be 1 or more'),),
    )
    image = models.ImageField(
        upload_to="recipes/images/", null=True, default=None
    )
    tags = models.ManyToManyField(
        Tag, verbose_name="Tag", related_query_name="Recipes"
    )
    ingredients = models.ManyToManyField(
        Ingredient, through="RecipeIngredient"
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Date created"
    )

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Ingredients in recipe db model class."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="Amounts",
        verbose_name="Recipe",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="Amounts",
        verbose_name="Ingredient",
    )
    amount = models.PositiveSmallIntegerField(
        "Amount",
        validators=(
            MinValueValidator(
                1, message='Amount should be 1 or more'),),
    )

    class Meta:
        verbose_name = "Ingredient in the recipe"
        verbose_name_plural = "Ingredients in the recipes"
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="this_ingredient_already_already_in_the_recipe",
            ),
        ]

    def __str__(self):
        return f"{self.amount} of {self.ingredient} in {self.recipe}"


class FavoriteRecipe(models.Model):
    """Favorite recipes db model class."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="Favorites",
        verbose_name="User",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="Users",
        verbose_name="Recipe",
    )

    class Meta:
        verbose_name = "Favorite Recipe"
        verbose_name_plural = "Favorite Recipes"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="already_favorite",
            ),
        ]

    def __str__(self):
        return f"{self.user} like {self.recipe.name}"


class CartRecipe(models.Model):
    """Recipes in the shopping cart db model class."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="ShoppingCart",
        verbose_name="User",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="ShoppingCart",
        verbose_name="Recipe",
    )

    class Meta:
        verbose_name = "Recipe in a shopping cart"
        verbose_name_plural = "Recipes in a shopping cart"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="already_in_the_cart",
            ),
        ]

    def __str__(self):
        return f"{self.user} like {self.recipe.name}"
