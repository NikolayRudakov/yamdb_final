from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import CurrentUserDefault
from rest_framework.validators import UniqueTogetherValidator, ValidationError

from .validators import UsernameNotMeValidator
from reviews.models import Comment, Review
from titles.models import Category, Genre, Title
from users.models import User


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        validators = [
            UsernameNotMeValidator(
                username="username",
            ),
        ]
        fields = ("username", "email")


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
    )
    confirmation_code = serializers.CharField(
        required=True,
    )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=["username", "email"],
            ),
        ]
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class UserMeSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ["role"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ("id",)
        lookup_field = "slug"
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ("id",)
        lookup_field = "slug"
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field="slug",
        many=True,
        queryset=Genre.objects.all(),
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = "__all__"


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        source="reviews__score__avg", read_only=True
    )
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field="username", read_only=True, default=CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ("title", "author")

    def validate(self, attrs):
        review = Review.objects.filter(
            title=self.context["view"].kwargs.get("title_id"),
            author=self.context["request"].user,
        )
        if review.exists() and self.context["request"].method == "POST":
            raise ValidationError("Вы уже написали отзыв!")
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("review", "author")
