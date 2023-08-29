from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRoles(models.TextChoices):
    """Roles for Custom User model."""

    USER = "user", _("User")
    ADMIN = "admin", _("Admin")


class User(AbstractUser):
    """Custom User model."""

    username = models.CharField(
        _("username"),
        max_length=settings.LIMIT_STRINGS,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and "
            "@/./+/-/_ only."
        ),
        validators=[
            RegexValidator(
                r"^[\w.@+-]+\Z",
                (
                    "Enter a valid username. "
                    "This value may contain only letters,"
                    "numbers and @/./+/-/_ characters."
                ),
                "invalid",
            )
        ],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(max_length=settings.LIMIT_STRINGS)
    last_name = models.CharField(max_length=settings.LIMIT_STRINGS)
    email = models.EmailField(
        verbose_name="Email",
        unique=True,
        max_length=254,
    )
    password = models.CharField(max_length=settings.LIMIT_STRINGS)
    role = models.CharField(
        default=UserRoles.USER,
        choices=UserRoles.choices,
        max_length=12,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def get_username(self):
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        constraints = [
            models.UniqueConstraint(
                fields=("username", "email"),
                name="unique_user",
            ),
        ]

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN or self.is_superuser

    @property
    def is_user(self):
        return self.role == UserRoles.USER

    def __str__(self):
        return f"{self.username} ({self.email})"


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Subscriber",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Author",
    )

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
        constraints = [
            models.CheckConstraint(
                check=~models.Q(author=models.F("user")),
                name="can_not_subscribe_to_yourself",
            ),
            models.UniqueConstraint(
                fields=["user", "author"], name="unique_subscription"
            ),
        ]

    def __str__(self):
        return f"{self.user} subscribed on {self.author}"
