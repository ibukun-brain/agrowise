from django.urls import path

from articles.api.views import ArticleDetailAPIView, ArticleListAPIView, CommentAPIView

app_name = "articles"

urlpatterns = [
    path(route="articles/", view=ArticleListAPIView.as_view(), name="articles"),
    path(
        route="articles/<slug:slug>/",
        view=ArticleDetailAPIView.as_view(),
        name="article",
    ),
    path(
        route="articles/<slug:slug>/comments/",
        view=CommentAPIView.as_view(),
        name="article",
    ),
]
