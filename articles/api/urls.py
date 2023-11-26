from django.urls import path

from articles.api.views import ArticleListAPIView, ArticleDetailAPIView

app_name = "articles"

urlpatterns = [
    path(
        route="articles/",
        view=ArticleListAPIView.as_view(),
        name="articles"
    ),
    path(
        route="articles/<slug:slug>/",
        view=ArticleDetailAPIView.as_view(),
        name="article"
    ),
]
