import random

from rest_framework.decorators import api_view, action
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly,
)

from recipes.models import Recipe, Tag, Ingredient, FavoriteRecipe, CartRecipe
from api.serializers import RecipeSerializer, TagSerializer, IngredientSerializer, FavoriteRecipeSerializer, CartRecipeSerializer
from api.permissions import IsAdminOrReadOnly, IsOwnerAdminOrReadOnly
from api.filters import IngredientSearchFilter, RecipeFilter
from api.paginator import RecipesPagination


class RecipeViewSet(viewsets.ModelViewSet):
    """
    API endpoint
    """
    http_method_names = ['get', 'post', 'patch', 'delete']
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

    @action(detail=True, methods=['post'], serializer_class=FavoriteRecipeSerializer)
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        # data = {'user': request.user.id, 'recipe': pk}
        # serializer = FavoriteRecipeSerializer(data=data, context={'request': request})
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        model_obj = get_object_or_404(FavoriteRecipe, user=user, recipe=recipe)
        model_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

 
class FavoriteRecipeViewSet(viewsets.ModelViewSet):
    """
    API endpoint
    """
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = FavoriteRecipe.objects.all()
    serializer_class = FavoriteRecipeSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def _get_recipe(self):
        recipe_id = self.kwargs.get("recipe_id")
        return get_object_or_404(Recipe, id=recipe_id)

    # def get_queryset(self):
    #     recipe = self._get_recipe()
    #     return recipe.Users.all()

    def perform_create(self, serializer):
        recipe = self._get_recipe()
        serializer.save(user=self.request.user, recipe=recipe)

    def perform_destroy(self, serializer):
        recipe = self._get_recipe()
        serializer.save(user=self.request.user, recipe=recipe)


class CartRecipeViewSet(viewsets.ModelViewSet):
    """
    API endpoint
    """
    http_method_names = ['post', 'delete']
    queryset = CartRecipe.objects.all()
    serializer_class = CartRecipeSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def _get_recipe(self):
        recipe_id = self.kwargs.get("recipe_id")
        return get_object_or_404(Recipe, id=recipe_id)

    # def get_queryset(self):
    #     recipe = self._get_recipe()
    #     return recipe.Users.all()

    def perform_create(self, serializer):
        recipe = self._get_recipe()
        serializer.save(user=self.request.user, recipe=recipe)

    def perform_destroy(self, serializer):
        recipe = self._get_recipe()
        serializer.save(user=self.request.user, recipe=recipe)


class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint
    """
    http_method_names = ['get']
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    """
    API endpoint
    """
    http_method_names = ['get']
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


@api_view(['GET'])
def test(request):
    return Response({'Случайное число': str(random.randint(1, 100))})
