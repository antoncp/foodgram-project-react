from django_filters import rest_framework as filter
from rest_framework import filters

from recipes.models import Recipe


class RecipeFilter(filter.FilterSet):
    """Custom filter for recipes endpoint."""
    tags = filter.CharFilter(field_name="tags__slug", lookup_expr="iexact")
    is_favorited = filter.BooleanFilter(method="filter_favorited")
    is_in_shopping_cart = filter.BooleanFilter(method="filter_shopping_cart")

    class Meta:
        model = Recipe
        fields = ["author", "tags", "is_favorited"]

    def filter_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(Users__user=self.request.user)
        return queryset

    def filter_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(ShoppingCart__user=self.request.user)
        return queryset


class IngredientSearchFilter(filters.SearchFilter):
    """Custom search filter for ingredients."""
    search_param = "name"
