from django.urls import include, path
from api.views import test
from rest_framework import routers
from api.views import RecipeViewSet, TagipeViewSet, IngredientViewSet

app_name = 'api'
router_v1 = routers.DefaultRouter()
router_v1.register(r'recipes', RecipeViewSet)
router_v1.register(r'tags', TagipeViewSet)
router_v1.register(r'ingredients', IngredientViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
    path('test/', test),
]
