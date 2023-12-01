from django.urls import path

from communities.api.views import (
    AllCommunitiesDetailAPIView,
    AllCommunitiesListAPIView,
    CommunityPostCommentCreateAPIView,
    CommunityPostCommentDetailAPIView,
    CommunityPostCommentUpdateAPIView,
    CommunityPostsListCreateAPIView,
    CommunityPostsRetrieveUpdateDestroyAPIView,
    JoinCommunityCreateAPIView,
    LeaveCommunityAPIView,
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
        route="community/<slug:slug>/",
        view=AllCommunitiesDetailAPIView.as_view(),
        name="community-detail",
    ),
    path(
        route="communities/me/",
        view=MyCommunitiesListCreateAPIView.as_view(),
        name="communities",
    ),
    path(
        route="community/<slug:slug>/posts/",
        view=CommunityPostsListCreateAPIView.as_view(),
        name="posts",
    ),
    path(
        route="community/<slug:slug>/posts/<uuid:uid>/comments/",
        view=CommunityPostCommentDetailAPIView.as_view(),
        name="community"
    ),
    path(
        route="community/<slug:slug>/posts/<uuid:uid>/",
        view=CommunityPostCommentCreateAPIView.as_view(),
        name="community"
    ),
    path(
        route="community/<slug:slug>/posts/<uuid:uid>/comments/<uuid:comment_uid>/",
        view=CommunityPostCommentUpdateAPIView.as_view(),
        name="community"
    ),
    path(
        route="community/<slug:slug>/posts/<uuid:uid>/",
        view=CommunityPostsRetrieveUpdateDestroyAPIView.as_view(),
        name="posts",
    ),
    path(
        route="community/<slug:slug>/join/",
        view=JoinCommunityCreateAPIView.as_view(),
        name="join-community",
    ),
    path(
        route="community/<slug:slug>/leave/",
        view=LeaveCommunityAPIView.as_view(),
        name="leave-community",
    ),
]
