import io

from api.filters import IngredientSearchFilter, RecipeFilter
from api.paginator import RecipesPagination
from api.permissions import IsAdminOrReadOnly, IsOwnerAdminOrReadOnly
from api.serializers import (CartRecipeSerializer, FavoriteRecipeSerializer,
                             IngredientSerializer, RecipeSerializer,
                             TagSerializer, FollowSerializer)
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (CartRecipe, FavoriteRecipe, Ingredient, Recipe,
                            RecipeIngredient, Tag)
from users.models import Follow
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
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

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        pdfmetrics.registerFont(
            TTFont("FreeSans", "foodgram_static/freesans.ttf", "UTF-8")
        )
        p.setFont("FreeSans", 24)
        p.setFillColorRGB(0, 0, 255)
        p.drawString(50, 770, "ИНГРЕДИЕНТЫ для покупки")
        p.setFillColorRGB(0, 0, 0)
        p.setFont("FreeSans", 14)
        p.drawString(50, 750, "(на основе рецептов в вашей корзине)")
        p.line(10, 725, 550, 725)
        ingredients = (
            RecipeIngredient.objects.filter(
                recipe__ShoppingCart__user=request.user
            )
            .values("ingredient__name", "ingredient__measurement_unit")
            .annotate(total_amount=Sum("amount"))
            .order_by("-total_amount")
        )
        pos_y = 700
        for num, ingredient in enumerate(ingredients, start=1):
            p.drawString(
                50,
                pos_y,
                (
                    f"{num}) {ingredient['ingredient__name']} "
                    f"{ingredient['total_amount']} "
                    f"{ingredient['ingredient__measurement_unit']}"
                ),
            )
            pos_y -= 25
        p.line(10, pos_y, 550, pos_y)
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(
            buffer, as_attachment=True, filename="shopping-list.pdf"
        )


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


class FollowViewSet(viewsets.ModelViewSet):
    """Follow API endpoint."""

    http_method_names = ["get"]
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.following.all()
