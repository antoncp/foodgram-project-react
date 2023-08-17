import base64

from django.core.files.base import ContentFile
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag, User
from rest_framework import serializers


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


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Ingredient model serializer."""
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(source='ingredient.measurement_unit')

    class Meta:
        fields = ("id", "name", "measurement_unit", "amount")
        model = RecipeIngredient


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
        )


class RecipeSerializer(serializers.ModelSerializer):
    """Recipe model serializer."""
    tags = TagSerializer(Tag.objects.all(), many=True)
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(source="Ingredients", many=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        fields = ("id", 'tags', "author", 'ingredients', "name", 'image', "text", 'cooking_time')
        read_only_fields = ("id", "author")
        model = Recipe

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for tag_data in tags_data:
            tag_id = tag_data['id']
            recipe.tags.add(tag_id)
        return recipe
