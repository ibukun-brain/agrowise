from rest_framework import filters, generics
from rest_framework.mixins import RetrieveModelMixin

from communities.api.serializers import (
    CommunityMembershipSerializer,
    CommunitySerializer,
)
from communities.models import Community, CommunityMembership


class AllCommunitiesListAPIView(generics.ListAPIView):
    serializer_class = CommunitySerializer
    search_fields = ["name"]
    filter_backends = [filters.SearchFilter]

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

    def get(self, request, *args, **kwargs):
        """
        Endpoint to get a single community
        """
        return self.retrieve(request, *args, **kwargs)

    def get_object(self):
        slug = self.kwargs["slug"]
        qs = (
            Community.objects.select_related("admin")
            .prefetch_related("members")
            .get(slug=slug)
        )
        return qs


class JoinCommunityCreateAPIView(RetrieveModelMixin, generics.CreateAPIView):
    serializer_class = CommunityMembershipSerializer

    # def get_queryset(self):
    #     qs = CommunityMembership.objects.select_related(
    #         'member', "community"
    #     ).all()
    #     return qs

    def get_object(self):
        slug = self.kwargs["slug"]
        qs = CommunityMembership.objects.select_related("member", "community").get(
            community__slug=slug
        )
        return qs

    def perform_create(self, serializer):
        slug = self.kwargs["slug"]
        community = (
            Community.objects.select_related("admin")
            .prefetch_related("members")
            .get(slug=slug)
        )
        serializer.save(member=self.request.user, community=community)


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
        qs = (
            Community.objects.select_related("admin")
            .prefetch_related("members")
            .filter(admin=self.request.user)
        )
        return qs

    def perform_create(self, serializer):
        serializer.save(admin=self.request.user)
