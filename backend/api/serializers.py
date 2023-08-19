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
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(source='ingredient.measurement_unit', read_only=True)

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
    is_subscribed = serializers.BooleanField(default='false')

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed'
        )


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email', 'username', 'first_name', 'last_name', 'password'
        )


class RecipeSerializer(serializers.ModelSerializer):
    """Recipe model serializer."""
    tags = serializers.SerializerMethodField()
    ingredients = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        fields = ("id", 'tags', "author", 'ingredients', "name", 'image', "text", 'cooking_time')
        read_only_fields = ("id", "author")
        model = Recipe

    def get_tags(self, obj):
        tags = obj.tags.all()
        return TagSerializer(tags, many=True).data

    def get_ingredients(self, obj):
        ingredients = RecipeIngredient.objects.filter(recipe=obj)
        return RecipeIngredientSerializer(ingredients, many=True).data

    def create(self, validated_data):
        tags_data = self.initial_data.get('tags', [])
        ingredients_data = self.initial_data.get('ingredients', [])
        recipe = Recipe.objects.create(**validated_data)
        for tag_data in tags_data:
            recipe.tags.add(tag_data)
        for ingredient_data in ingredients_data:
            ingredient_id = ingredient_data.get('id')
            amount = ingredient_data.get('amount')
            RecipeIngredient.objects.create(recipe=recipe, ingredient_id=ingredient_id, amount=amount)
        return recipe
