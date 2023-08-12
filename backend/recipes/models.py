from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Recipe(models.Model):
    """Recipe db model class."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="Recipes",
        verbose_name="Author",
    )
    name = models.CharField(
        'Name',
        max_length=200
    )
    text = models.TextField(
        'Text',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Cooking time',
    )   

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return self.name
