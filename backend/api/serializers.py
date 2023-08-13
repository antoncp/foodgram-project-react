from django.contrib.auth.models import User, Group
from rest_framework import serializers

from recipes.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """Recipe model serializer."""

    class Meta:
        fields = ("id", "text", "author", "name")
        read_only_fields = ("id", "author", "name")
        model = Recipe
