from unicodedata import category

from rest_framework import generics, permissions
from rest_framework.mixins import RetrieveModelMixin

from articles.api.serializers import ArticleCommentSerializer, ArticleSerializer
from articles.models import Article


class ArticleListAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ArticleSerializer

    def get_queryset(self):
        qs = Article.objects.select_related('author', "category") \
            .prefetch_related("comments").filter(status="ready")
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
        slug = self.kwargs['slug']
        qs = Article.objects.select_related('author').get(slug=slug)
        return qs
