from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .filters import TitlesFilter
from .mixins import GetPostDelMixin
from .pagination import ApiPagination
from .permissions import AuthorOrAdminOrReadOnly, IsAdmin, IsAdminOrReadOnly
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReadOnlyTitleSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleSerializer,
    TokenSerializer,
    UserMeSerializer,
    UserSerializer,
)
from reviews.models import Review
from titles.models import Category, Genre, Title
from users.confirm_code_generator import confirm_code_generator
from users.models import User


class SignUp(APIView):
    """Вью для регистрации"""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        confirm_code_generator(user)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class Token(APIView):
    """Вью для токенов"""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=serializer.validated_data["username"]
        )
        confirmation_code = serializer.validated_data["confirmation_code"]
        if confirmation_code == confirm_code_generator(user):
            token = {"token": str(AccessToken.for_user(user))}
            return Response(token, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для пользователей"""

    queryset = User.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = UserSerializer
    pagination_class = ApiPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["username"]
    lookup_field = "username"

    @action(
        methods=["get", "patch"],
        detail=False,
        url_path="me",
        permission_classes=[IsAuthenticated],
    )
    def user_me_actions(self, request):
        user = self.request.user
        if request.method == "GET":
            serializer = UserMeSerializer(user)
            return Response(serializer.data)
        if request.method == "PATCH":
            user = self.request.user
            serializer = UserMeSerializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class CategoryViewSet(GetPostDelMixin):
    """Вьюсет для категорий"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = ApiPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class GenreViewSet(GetPostDelMixin):
    """Вьюсет для жанров"""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = ApiPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений"""

    queryset = (
        Title.objects.all().annotate(Avg("reviews__score")).order_by("name")
    )
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = ApiPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return ReadOnlyTitleSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов"""

    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrAdminOrReadOnly,)
    pagination_class = ApiPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев"""

    serializer_class = CommentSerializer
    permission_classes = (AuthorOrAdminOrReadOnly,)
    pagination_class = ApiPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        review = get_object_or_404(
            Review, id=self.kwargs.get("review_id"), title=title
        )
        return review.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        review = get_object_or_404(
            Review, pk=self.kwargs.get("review_id"), title=title
        )
        serializer.save(author=self.request.user, review=review)
