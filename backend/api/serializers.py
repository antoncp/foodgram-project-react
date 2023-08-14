from django.contrib.auth.models import User
from rest_framework import serializers

from recipes.models import Recipe, Tag, Ingredient


class TagSerializer(serializers.ModelSerializer):
    """Tag model serializer."""

    class Meta:
        fields = ("id", "name", "color", "slug")
        read_only_fields = ("id", "name")
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    """Ingredient model serializer."""

    class Meta:
        fields = ("id", "name", "measurement_unit")
        read_only_fields = ("id", "name")
        model = Ingredient


class RecipeSerializer(serializers.ModelSerializer):
    """Recipe model serializer."""
    tag = Tag.objects.all()
    # ingredient = Ingredient.objects.all()
    tags = TagSerializer(
        tag,
        many=True,
    )
    # ingredients = IngredientSerializer(
    #     ingredient,
    #     many=True,
    # )

    class Meta:
        fields = ("id", "name", "text", "author", 'image', 'tags', 'ingredients')
        read_only_fields = ("id", "author", "name")
        model = Recipe