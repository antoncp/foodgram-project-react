from rest_framework import filters
from django_filters import rest_framework as filter

from recipes.models import Recipe


class RecipeFilter(filter.FilterSet):
    tags = filter.CharFilter(field_name='tags__slug', lookup_expr='iexact')

    class Meta:
        model = Recipe
        fields = ['author', 'tags']


class IngredientSearchFilter(filters.SearchFilter):
    search_param = "name"
