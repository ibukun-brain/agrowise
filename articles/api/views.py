from rest_framework import generics, permissions

from articles.api.serializers import (
    ArticleCommentSerializer,
    ArticleSerializer,
    UserArticleCommentSerializer,
)
from articles.models import Article, Comment


class ArticleListAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ArticleSerializer

    def get_queryset(self):
        qs = (
            Article.objects.select_related("author", "category")
            .prefetch_related("comments")
            .filter(status="published")
        )
        return qs

    def get(self, request, *args, **kwargs):
        """
        This Endpoint returns all articles
        """
        return self.list(request, *args, **kwargs)


class ArticleDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ArticleCommentSerializer
    permission_classes = [permissions.AllowAny]
    lookup_url_kwarg = "slug"

    def get_object(self):
        slug = self.kwargs["slug"]
        qs = (
            Article.objects.select_related("author", "category")
            .prefetch_related("comments")
            .get(slug=slug)
        )
        return qs

    def get(self, request, *args, **kwargs):
        """
        This Endpoint returns a single article
        """
        return self.retrieve(request, *args, **kwargs)


class CommentAPIView(generics.CreateAPIView):
    serializer_class = UserArticleCommentSerializer

    def get_queryset(self):
        qs = Comment.objects.select_related("article", "user").all()
        return qs

    def post(self, request, *args, **kwargs):
        """
        This endpoint creates a comment for an article
        """
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        slug = self.kwargs["slug"]
        article = (
            Article.objects.select_related("author", "category")
            .prefetch_related("comments")
            .get(slug=slug)
        )
        serializer.save(user=self.request.user, article=article)
