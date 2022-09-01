from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from titles.models import Title
from users.models import User


class Review(models.Model):
    """Модель отзывов на произведения"""

    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        db_index=True,
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        db_index=True,
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(1, message="Минимальная оценка - 1"),
            MaxValueValidator(10, message="Максимальная оценка - 10"),
        ],
        blank=True,
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ("-pub_date",)
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"],
                name="unique_review",
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментариев"""

    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        db_index=True,
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        db_index=True,
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("-pub_date",)

    def __str__(self):
        return self.text
