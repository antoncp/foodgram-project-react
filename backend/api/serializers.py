import base64

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.validators import EmailValidator, RegexValidator
from rest_framework import serializers

from recipes.models import (
    CartRecipe,
    FavoriteRecipe,
    Ingredient,
    Recipe,
    RecipeIngredient,
    Tag,
)
from users.models import User, Follow


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
        """Validates that new record is not already exist."""
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
                "This recipe is already in your list/cart"
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


class SmallRecipeSerializer(serializers.ModelSerializer):
    """Small Recipe model serializer for other serializers."""

    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class UserSerializer(serializers.ModelSerializer):
    """Custom user model serializer."""

    is_subscribed = serializers.SerializerMethodField()

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

    def get_is_subscribed(self, obj):
        request = self.context["request"]
        author = obj.id
        user = request.user
        return (
            user.is_authenticated
            and Follow.objects.filter(user=user, author=author).exists()
        )


class CreateUserSerializer(serializers.ModelSerializer):
    """Create custom user serializer."""

    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name", "password")

    def validate_email(self, value):
        if not EmailValidator(value):
            raise serializers.ValidationError(
                detail={"email": "Provide the correct email"}
            )
        return value

    def validate_username(self, value):
        validate_re = RegexValidator(
            r"^[\w.@+-]+\Z", "Letters, digits and @/./+/-/_ only"
        )
        validate_re(value)
        return value

    def validate_first_name(self, value):
        if len(value) > settings.LIMIT_STRINGS:
            raise serializers.ValidationError(
                detail={
                    "first_name": "Name should be shorter than 150 letters"
                }
            )
        return value

    def validate_last_name(self, value):
        if len(value) > settings.LIMIT_STRINGS:
            raise serializers.ValidationError(
                detail={
                    "last_name": "Last name should be shorter than 150 letters"
                }
            )
        return value

    def validate_password(self, value):
        if len(value) > settings.LIMIT_STRINGS:
            raise serializers.ValidationError(
                detail={
                    "password": "Password should be shorter than 150 letters"
                }
            )
        return value

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class FollowSerializer(UserSerializer):
    """Follow model serializer."""

    id = serializers.PrimaryKeyRelatedField(source="author.id", read_only=True)
    email = serializers.CharField(source="author.email", read_only=True)
    username = serializers.CharField(source="author.username", read_only=True)
    first_name = serializers.CharField(
        source="author.first_name", read_only=True
    )
    last_name = serializers.CharField(
        source="author.last_name", read_only=True
    )
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )

    def get_recipes(self, obj):
        limit_size = self.context["request"].query_params.get("recipes_limit")
        if limit_size.isdigit():
            recipes = Recipe.objects.filter(author=obj.author)[
                : int(limit_size)
            ]
        else:
            recipes = Recipe.objects.filter(author=obj.author)
        return SmallRecipeSerializer(recipes, many=True).data

    def get_is_subscribed(self, obj):
        request = self.context["request"]
        author = obj.author
        user = request.user
        return (
            user.is_authenticated
            and Follow.objects.filter(user=user, author=author).exists()
        )

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()

    def validate(self, data):
        """Validates that new record is not already exist."""
        request = self.context["request"]
        user = request.user
        author_id = self.context["view"].kwargs.get("user_id")
        if (
            request.method == "POST"
            and self.Meta.model.objects.filter(
                user=user, author=author_id
            ).exists()
        ):
            raise serializers.ValidationError(
                "This author is already in subscription list"
            )
        if user.id == int(author_id):
            raise serializers.ValidationError(
                "You can not subscribe to yourself"
            )
        return data


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
        return (
            user.is_authenticated
            and FavoriteRecipe.objects.filter(
                user=user, recipe=recipe
            ).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        request = self.context["request"]
        recipe = obj.id
        user = request.user
        return (
            user.is_authenticated
            and CartRecipe.objects.filter(user=user, recipe=recipe).exists()
        )

    def create(self, validated_data):
        """Creates a new recipe instance, all validation in the separate
        validate method (line 362).
        """
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

    def validate(self, data):
        """Validates all data in the recipe"""
        tags = self.initial_data.get("tags", [])
        if len(tags) != len(set(tags)):
            raise serializers.ValidationError(
                detail={"tags": "The tags in one recipe should be unique"}
            )
        for tag in tags:
            if not Tag.objects.filter(id=tag).exists():
                raise serializers.ValidationError(
                    detail={"tags": f"Tag with ID: {tag} does not exist"}
                )

        ingredients = self.initial_data.get("ingredients", [])
        ingredients_in_recipe = []
        for ingredient in ingredients:
            ingredient_id = ingredient.get("id")
            amount = ingredient.get("amount")
            if ingredient_id in ingredients_in_recipe:
                raise serializers.ValidationError(
                    detail={"ingredient": "Repeating ingredient"}
                )
            ingredients_in_recipe.append(ingredient_id)
            if int(amount) < 1:
                raise serializers.ValidationError(
                    detail={"amount": "Should be 1 or more"}
                )
            if not Ingredient.objects.filter(id=ingredient_id).exists():
                raise serializers.ValidationError(
                    detail={
                        "ingredient": (f"Ingredient with ID: "
                                       f"{ingredient_id} does not exist")
                    }
                )

        name = data["name"]
        if len(name) > settings.LIMIT_RECIPE_NAME:
            raise serializers.ValidationError(
                detail={"name": "Name should be shorter than 200 letters"}
            )

        cooking_time = data["cooking_time"]
        if int(cooking_time) <= 0:
            raise serializers.ValidationError(
                detail={"cooking_time": "Cooking time should be more than 0"}
            )
        return data
