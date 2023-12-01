from drf_spectacular.utils import OpenApiResponse, extend_schema
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from rest_framework import filters, generics, permissions, status
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from communities.api.serializers import (
    CommunityCommentSerializer,
    CommunityMembershipSerializer,
    CommunityPostCommentSerializer,
    CommunityPostSerializer,
    CommunitySerializer,
)
from communities.models import (
    Community,
    CommunityMembership,
    CommunityPost,
    CommunityPostComment,
)
from home.api.custom_permissions import IsOwnerOrReadOnly


class AllCommunitiesListAPIView(generics.ListAPIView):
    serializer_class = CommunitySerializer
    search_fields = ["name"]
    filter_backends = [filters.SearchFilter]

    @extend_schema(
        summary="Get all communities",
        request=CommunitySerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(description="Success"),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="You are unauthorized to access this endpoint"
            ),
        },
        # more customizations
    )
    def get(self, request, *args, **kwargs):
        """
        Endpoint to Return all communities.
        """
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        qs = Community.objects.select_related("admin").prefetch_related("members").all()
        return qs


class AllCommunitiesDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CommunitySerializer
    queryset = Community.objects.all()

    def get(self, request, *args, **kwargs):
        """
        Endpoint to get a single community
        """
        return self.retrieve(request, *args, **kwargs)

    def get_object(self):
        slug = self.kwargs["slug"]
        try:
            qs = (
                Community.objects.select_related("admin")
                .prefetch_related("members")
                .get(slug=slug)
            )
        except Community.DoesNotExist as e:
            raise ValidationError({"error": "community does not exist!"}) from e
        return qs


class JoinCommunityCreateAPIView(generics.CreateAPIView):
    serializer_class = CommunityMembershipSerializer

    def post(self, request, *args, **kwargs):
        """
        Endpoint to join a community
        """
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        slug = self.kwargs["slug"]
        community = Community()
        try:
            community = (
                Community.objects.select_related("admin")
                .prefetch_related("members")
                .get(slug=slug)
            )
        except Community.DoesNotExist as e:
            raise ValidationError({"error": "community does not exist!"}) from e
        serializer.save(member=self.request.user, community=community)


class LeaveCommunityAPIView(UpdateModelMixin, generics.GenericAPIView):
    serializer_class = CommunityMembershipSerializer

    def get_object(self):
        slug = self.kwargs["slug"]
        community = Community()
        try:
            community = (
                Community.objects.select_related("admin")
                .prefetch_related("members")
                .get(slug=slug)
            )
        except Community.DoesNotExist as e:
            raise ValidationError({"detail": "community does not exist!"}) from e
        try:
            community_membership = CommunityMembership.objects.get(
                community=community, member=self.request.user
            )
        except CommunityMembership.DoesNotExist as e:
            raise ValidationError(
                {"detail": "You are not a member of this community"}
            ) from e
        return community_membership

    def put(self, request, *args, **kwargs):
        """
        Endpoint to leave a community
        """
        partial = kwargs.pop("partial", False)
        serializer = CommunityMembershipSerializer(
            instance=self.get_object(), data=request.data, partial=partial
        )
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return Response(
                {"detail": "You have successfully leave this community"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"detail": "Cannot process this request"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class MyCommunitiesListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommunitySerializer
    search_fields = ["name"]
    filter_backends = [filters.SearchFilter]

    def get(self, request, *args, **kwargs):
        """
        Endpoint to return a specific communities created by a user
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Endpoint to create a community.
        Note: the user has to be logged in.
        """
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        qs = Community()
        try:
            qs = (
                Community.objects.select_related("admin")
                .prefetch_related("members")
                .filter(admin=self.request.user)
            )
        except Community.DoesNotExist:
            pass
        return qs

    def perform_create(self, serializer):
        serializer.save(admin=self.request.user)


class CommunityPostsListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommunityPostSerializer
    queryset = CommunityPost.objects.none()

    def get_queryset(self):
        slug = self.kwargs["slug"]
        try:
            qs = CommunityPost.objects.select_related("community", "owner").filter(
                community__slug=slug
            )
        except CommunityPost.DoesNotExist as e:
            raise ValidationError(
                {"error": "community does not exist"}, code="not found"
            ) from e

        return qs

    def get_object(self):
        slug = self.kwargs["slug"]
        try:
            qs = (
                Community.objects.select_related("admin")
                .prefetch_related("members")
                .get(slug=slug)
            )
        except Community.DoesNotExist as e:
            raise ValidationError(
                {"error": "community does not exist"}, code="not found"
            ) from e
        return qs

    def get(self, request, *args, **kwargs):
        """
        Endpoint to get all post in a community.
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Endpoint to create a post in a community.
        Note this user must be a memeber of the community
        """
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(community=self.get_object(), owner=user)


class CommunityPostsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommunityPostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_url_kwarg = "uid"

    def get_object(self):
        uid = self.kwargs["uid"]
        qs = CommunityPost.objects.get(uid=uid)
        hit_count = HitCount.objects.get_for_object(qs)
        hit_count_response = HitCountMixin.hit_count(self.request, hit_count)
        print(hit_count_response)
        return qs

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method in permissions.SAFE_METHODS:
            return CommunityPostCommentSerializer

        return self.serializer_class

    def get(self, request, *args, **kwargs):
        """
        Endpoint to get a single post in a community.
        """
        return self.retrieve(request, *args, **kwargs)

    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(community=self.get_object(), owner=user)

    def delete(self, request, *args, **kwargs):
        """
        Endpoint to delete a post in a community
        """
        return self.destroy(request, *args, **kwargs)


class CommunityPostCommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommunityCommentSerializer
    lookup_url_kwarg = "uid"

    def get_object(self):
        uid = self.kwargs["uid"]
        qs = (
            CommunityPost.objects.select_related(
                "community", "owner", "community__admin"
            )
            .prefetch_related("comments__user")
            .get(uid=uid)
        )
        return qs

    def get_queryset(self):
        uid = self.kwargs["uid"]
        qs = CommunityPostComment.objects.select_related(
            "community_post",
            "user",
            "community_post__owner",
            "community_post__community",
        ).filter(community_post__uid=uid)
        return qs

    def post(self, request, *args, **kwargs):
        """
        Endpoint for creating a new comment
        """
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(community_post=self.get_object(), user=self.request.user)


class CommunityPostCommentUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = CommunityCommentSerializer
    lookup_url_kwarg = "comment_uid"

    def get_object(self):
        uid = self.kwargs["comment_uid"]
        qs = CommunityPostComment.objects.select_related(
            "community_post",
            "user",
            "community_post__owner",
            "community_post__community",
        ).get(uid=uid)
        return qs

    def put(self, request, *args, **kwargs):
        """
        Endpoint to update a comment
        """
        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save(community_post=self.get_object(), user=self.request.user)
