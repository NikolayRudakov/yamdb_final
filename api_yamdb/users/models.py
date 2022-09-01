from django.contrib.auth.models import AbstractUser
from django.db import models

USER = "user"
MODERATOR = "moderator"
ADMIN = "admin"
ROLES = [
    (USER, "пользователь"),
    (MODERATOR, "модератор"),
    (ADMIN, "администратор"),
]


class User(AbstractUser):
    """Модель пользователя."""

    username = models.CharField(
        verbose_name="Имя пользователя",
        max_length=150,
        unique=True,
        db_index=True,
    )
    email = models.EmailField(
        verbose_name="email адрес",
        max_length=255,
        unique=True,
        db_index=True,
    )
    first_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    role = models.SlugField(choices=ROLES, default=USER)

    def __str__(self):
        return self.username

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser
