from django.contrib.auth import get_user_model
from django.db import models

from .validators import validate_year

User = get_user_model()


class Category(models.Model):
    """Модель категорий"""

    name = models.CharField(
        max_length=256,
        verbose_name="Категория",
        unique=True,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров"""

    name = models.CharField(
        max_length=256,
        verbose_name="Категория",
        unique=True,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений"""

    name = models.CharField(
        max_length=256,
        verbose_name="Произведение",
    )
    year = models.IntegerField(
        null=True, verbose_name="Год издания", validators=[validate_year]
    )
    description = models.CharField(
        max_length=400,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name="titles",
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name="titles",
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
