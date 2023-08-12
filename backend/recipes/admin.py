from django.contrib import admin

from .models import Recipe


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author', 'text', 'cooking_time')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-empty-'


admin.site.register(Recipe, RecipeAdmin)
