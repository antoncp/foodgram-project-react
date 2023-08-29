from django.urls import include, path
from rest_framework import routers

from api.views import (FollowViewSet, IngredientViewSet, RecipeViewSet,
                       TagViewSet)

app_name = "api"

router_v1 = routers.DefaultRouter()
router_v1.register(r"recipes", RecipeViewSet)
router_v1.register(r"tags", TagViewSet)
router_v1.register(r"ingredients", IngredientViewSet)
router_v1.register(r"users/subscriptions", FollowViewSet, basename="following")

category_detail = FollowViewSet.as_view(
    {
        "post": "create",
        "delete": "destroy",
    }
)

urlpatterns = [
    path(
        "users/<int:user_id>/subscribe/", category_detail, name="subscriptions"
    ),
    path("", include(router_v1.urls)),
    path("", include('djoser.urls')),
    path("auth/", include('djoser.urls.authtoken')),
]
