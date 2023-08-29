from django.contrib import admin

from .models import Follow, User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "username",
        "first_name",
        "last_name",
        "email",
        "role",
    )
    list_display_links = ("username",)
    list_filter = ("email", "first_name")


class FollowAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "author")
    search_fields = ("author",)
    list_filter = ("author",)
    empty_value_display = "None"


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
