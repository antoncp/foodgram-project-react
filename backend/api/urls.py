from django.urls import include, path
from rest_framework import routers
from api.views import RecipeViewSet, TagViewSet, IngredientViewSet, FavoriteRecipeViewSet, CartRecipeViewSet

app_name = 'api'

# favorite_recipe_viewset = FavoriteRecipeViewSet.as_view({'post': 'create', 'delete': 'destroy'})

router_v1 = routers.DefaultRouter()
router_v1.register(
    r"recipes/(?P<recipe_id>\d+)/shopping_cart",
    CartRecipeViewSet,
    basename='CartRecipe'
)
router_v1.register(r'recipes', RecipeViewSet)
router_v1.register(r'tags', TagViewSet)
router_v1.register(r'ingredients', IngredientViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
]
