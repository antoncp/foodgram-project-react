import random

from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from recipes.models import Recipe, Tag, Ingredient
from api.serializers import RecipeSerializer, TagSerializer, IngredientSerializer
from api.permissions import IsAdminOrReadOnly


class RecipeViewSet(viewsets.ModelViewSet):
    """
    API endpoint
    """
    http_method_names = ['get', 'post', 'patch']
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagipeViewSet(viewsets.ModelViewSet):
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


@api_view(['GET'])
def test(request):
    return Response({'Случайное число': str(random.randint(1, 100))})
