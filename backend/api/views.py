from api.filters import IngredientSearchFilter, RecipeFilter
from api.paginator import RecipesPagination
from api.permissions import IsAdminOrReadOnly, IsOwnerAdminOrReadOnly
from api.serializers import (CartRecipeSerializer, FavoriteRecipeSerializer,
                             IngredientSerializer, RecipeSerializer,
                             TagSerializer)
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import CartRecipe, FavoriteRecipe, Ingredient, Recipe, Tag
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response


class RecipeViewSet(viewsets.ModelViewSet):
    """Recipes API endpoint."""

    http_method_names = ["get", "post", "patch", "delete"]
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAdminOrReadOnly, IsOwnerAdminOrReadOnly)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = RecipesPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=["post"],
        serializer_class=FavoriteRecipeSerializer,
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        model_obj = get_object_or_404(FavoriteRecipe, user=user, recipe=recipe)
        model_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True, methods=["post"], serializer_class=CartRecipeSerializer
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        model_obj = get_object_or_404(CartRecipe, user=user, recipe=recipe)
        model_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ModelViewSet):
    """Tags API endpoint."""

    http_method_names = ["get"]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    """Ingredients API endpoint."""

    http_method_names = ["get"]
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None
    filter_backends = (IngredientSearchFilter,)
    search_fields = ("^name",)
