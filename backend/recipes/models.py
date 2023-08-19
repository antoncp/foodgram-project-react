from django.db import models

from users.models import User


class Tag(models.Model):
    """Tag db model class."""

    name = models.CharField(
        'Name',
        max_length=256,
        unique=True,
    )
    color = models.CharField(
        'Color',
        max_length=16
    )
    slug = models.SlugField(
        'Slug',
        max_length=50,
        unique=True,
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient db model class."""

    name = models.CharField(
        'Name',
        max_length=256
    )
    measurement_unit = models.CharField(
        'Measurement unit',
        max_length=256
    )

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
    name = models.CharField(
        'Name',
        max_length=200
    )
    text = models.TextField(
        'Text',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Cooking time',
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Tag',
        related_query_name='Recipes'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient"
    )

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

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
        'Amount',
    )

    def __str__(self):
        return f'{self.amount} of {self.ingredient} in {self.recipe}'


class FavoriteRecipe(models.Model):
    """Recipe db model class."""

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
        verbose_name = 'Favorite Recipe'
        verbose_name_plural = 'Favorite Recipes'
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="already_favorite",
            ),
        ]

    def __str__(self):
        return f'{self.user} like {self.recipe.name}'


class CartRecipe(models.Model):
    """Recipe db model class."""

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
        verbose_name = 'Recipe in a shopping cart'
        verbose_name_plural = 'Recipes in a shopping cart'
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="already_in_the_cart",
            ),
        ]

    def __str__(self):
        return f'{self.user} like {self.recipe.name}'
