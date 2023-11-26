from django.urls import path

from communities.api.views import (
    AllCommunitiesDetailAPIView,
    AllCommunitiesListAPIView,
    JoinCommunityCreateAPIView,
    MyCommunitiesListCreateAPIView,
)

app_name = "communities"

urlpatterns = [
    path(
        route="communities/",
        view=AllCommunitiesListAPIView.as_view(),
        name="communities",
    ),
    path(
        route="communities/<slug:slug>/",
        view=AllCommunitiesDetailAPIView.as_view(),
        name="community-detail",
    ),
    path(
        route="communities/me/",
        view=MyCommunitiesListCreateAPIView.as_view(),
        name="communities",
    ),
    path(
        route="communities/<slug:slug>/join/",
        view=JoinCommunityCreateAPIView.as_view(),
        name="join-community",
    ),
]
