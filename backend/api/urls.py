from django.urls import include, path
from rest_framework import routers
from api.views import RecipeViewSet, TagViewSet, IngredientViewSet

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register(r'recipes', RecipeViewSet)
router_v1.register(r'tags', TagViewSet)
router_v1.register(r'ingredients', IngredientViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
]
