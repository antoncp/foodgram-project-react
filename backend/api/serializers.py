import base64

from django.core.files.base import ContentFile
from recipes.models import (FavoriteRecipe, Ingredient, Recipe,
                            RecipeIngredient, Tag, User, CartRecipe)
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


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    """Ingredient """
    id = serializers.PrimaryKeyRelatedField(source='recipe.id', read_only=True)
    name = serializers.CharField(source='recipe.name', read_only=True)
    image = serializers.ImageField(source='recipe.image', read_only=True)
    cooking_time = serializers.IntegerField(source='recipe.cooking_time', read_only=True)

    class Meta:
        fields = ("id", "name", "image", "cooking_time")
        read_only_fields = ("id", "name", "image", "cooking_time")
        model = FavoriteRecipe

    def validate(self, data):
        """Validate that """
        request = self.context['request']
        user = request.user
        recipe_id = self.context['view'].kwargs.get('pk')
        if (request.method == 'POST'
           and FavoriteRecipe.objects.filter(user=user, recipe=recipe_id).exists()):
            raise serializers.ValidationError(
                'This recipe already in your favorite list'
            )
        return data


class CartRecipeSerializer(serializers.ModelSerializer):
    """Ingredient """
    id = serializers.PrimaryKeyRelatedField(source='recipe.id', read_only=True)
    name = serializers.CharField(source='recipe.name', read_only=True)
    image = serializers.ImageField(source='recipe.image', read_only=True)
    cooking_time = serializers.IntegerField(source='recipe.cooking_time', read_only=True)

    class Meta:
        fields = ("id", "name", "image", "cooking_time")
        read_only_fields = ("id", "name", "image", "cooking_time")
        model = CartRecipe

    def validate(self, data):
        """Validate that """
        request = self.context['request']
        recipe_id = self.context['view'].kwargs.get('recipe_id')
        user = request.user
        if (request.method == 'POST'
           and CartRecipe.objects.filter(user=user, recipe=recipe_id).exists()):
            raise serializers.ValidationError(
                'This recipe already in your shopping cart'
            )
        return data


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
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        fields = ("id", 'tags', "author", 'ingredients', "is_favorited", "is_in_shopping_cart", "name", 'image', "text", 'cooking_time')
        read_only_fields = ("id", "author")
        model = Recipe

    def get_tags(self, obj):
        tags = obj.tags.all()
        return TagSerializer(tags, many=True).data

    def get_ingredients(self, obj):
        ingredients = RecipeIngredient.objects.filter(recipe=obj)
        return RecipeIngredientSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        request = self.context['request']
        recipe = obj.id
        user = request.user
        if user.is_authenticated and FavoriteRecipe.objects.filter(user=user, recipe=recipe).exists():
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        request = self.context['request']
        recipe = obj.id
        user = request.user
        if user.is_authenticated and CartRecipe.objects.filter(user=user, recipe=recipe).exists():
            return True
        return False

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
