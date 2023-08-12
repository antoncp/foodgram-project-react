import random

from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from recipes.models import Recipe
from api.serializers import RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """
    API endpoint 
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.AllowAny]


@api_view(['GET'])
def test(request):
    return Response({'Случайное число': str(random.randint(1, 100))})

