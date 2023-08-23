from rest_framework.pagination import PageNumberPagination


class RecipesPagination(PageNumberPagination):
    """Custom pagination class for recipes."""
    page_size_query_param = 'limit'
