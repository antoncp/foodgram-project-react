import base64

from django.core.files.base import ContentFile
from recipes.models import (CartRecipe, FavoriteRecipe, Ingredient, Recipe,
                            RecipeIngredient, Tag, User)
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
    """Ingredients amount in the recipe model serializer."""

    id = serializers.IntegerField(source="ingredient.id")
    name = serializers.CharField(source="ingredient.name", read_only=True)
    measurement_unit = serializers.CharField(
        source="ingredient.measurement_unit", read_only=True
    )

    class Meta:
        fields = ("id", "name", "measurement_unit", "amount")
        model = RecipeIngredient


class CartFavoriteRecipeSerializer(serializers.ModelSerializer):
    """Base serializer for Carts and Favorites."""

    id = serializers.PrimaryKeyRelatedField(source="recipe.id", read_only=True)
    name = serializers.CharField(source="recipe.name", read_only=True)
    image = serializers.ImageField(source="recipe.image", read_only=True)
    cooking_time = serializers.IntegerField(
        source="recipe.cooking_time", read_only=True
    )

    def validate(self, data):
        """Validate that"""
        request = self.context["request"]
        user = request.user
        recipe_id = self.context["view"].kwargs.get("pk")
        if (
            request.method == "POST"
            and self.Meta.model.objects.filter(
                user=user, recipe=recipe_id
            ).exists()
        ):
            raise serializers.ValidationError(
                "This recipe already in your favorite list"
            )
        return data


class FavoriteRecipeSerializer(CartFavoriteRecipeSerializer):
    """FavoriteRecipe model serializer."""

    class Meta:
        fields = ("id", "name", "image", "cooking_time")
        read_only_fields = ("id", "name", "image", "cooking_time")
        model = FavoriteRecipe


class CartRecipeSerializer(CartFavoriteRecipeSerializer):
    """CartRecipe model serializer."""

    class Meta:
        fields = ("id", "name", "image", "cooking_time")
        read_only_fields = ("id", "name", "image", "cooking_time")
        model = CartRecipe


class Base64ImageField(serializers.ImageField):
    """Base64ImageField serializer."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]

            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)

        return super().to_internal_value(data)


class UserSerializer(serializers.ModelSerializer):
    """Custom user model serializer."""

    is_subscribed = serializers.BooleanField(default="false")

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )


class CreateUserSerializer(serializers.ModelSerializer):
    """Create custom user serializer."""

    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name", "password")


class RecipeSerializer(serializers.ModelSerializer):
    """Recipe model serializer."""

    tags = serializers.SerializerMethodField()
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )
        read_only_fields = ("id", "author")
        model = Recipe

    def get_tags(self, obj):
        tags = obj.tags.all()
        return TagSerializer(tags, many=True).data

    def get_ingredients(self, obj):
        ingredients = RecipeIngredient.objects.filter(recipe=obj)
        return RecipeIngredientSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        request = self.context["request"]
        recipe = obj.id
        user = request.user
        if (
            user.is_authenticated
            and FavoriteRecipe.objects.filter(
                user=user, recipe=recipe
            ).exists()
        ):
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        request = self.context["request"]
        recipe = obj.id
        user = request.user
        if (
            user.is_authenticated
            and CartRecipe.objects.filter(user=user, recipe=recipe).exists()
        ):
            return True
        return False

    def create(self, validated_data):
        tags_data = self.initial_data.get("tags", [])
        ingredients_data = self.initial_data.get("ingredients", [])
        recipe = Recipe.objects.create(**validated_data)
        for tag_data in tags_data:
            recipe.tags.add(tag_data)
        for ingredient_data in ingredients_data:
            ingredient_id = ingredient_data.get("id")
            amount = ingredient_data.get("amount")
            RecipeIngredient.objects.create(
                recipe=recipe, ingredient_id=ingredient_id, amount=amount
            )
        return recipe

    def update(self, instance, validated_data):
        tags_data = self.initial_data.get("tags", [])
        ingredients_data = self.initial_data.get("ingredients", [])
        instance.tags.clear()
        instance.ingredients.clear()
        super().update(instance, validated_data)
        for tag_data in tags_data:
            instance.tags.add(tag_data)
        for ingredient_data in ingredients_data:
            ingredient_id = ingredient_data.get("id")
            amount = ingredient_data.get("amount")
            RecipeIngredient.objects.create(
                recipe=instance, ingredient_id=ingredient_id, amount=amount
            )
        return instance

    def validate_name(self, value):
        if len(value) > 200:
            raise serializers.ValidationError(
                detail={"name": "Name should be shorter than 200 letters"}
            )
        return value

    def validate_cooking_time(self, value):
        if int(value) <= 0:
            raise serializers.ValidationError(
                detail={"cooking_time": "Cooking time should be more than 0"}
            )
        return value
