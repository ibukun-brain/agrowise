from rest_framework import generics, permissions

from farms.api.serializers import FarmSerializer, ProduceListingSerializer
from farms.models import Farm, ProduceListing
from home.api.custom_permissions import IsOwnerOrReadOnly


class FarmListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = FarmSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        qs = Farm.objects.select_related("owner") \
            .filter(owner=self.request.user)
        return qs

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        """
        This endpoint returns farm/farms for a loggedin user
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        This endpoint for creates farms for user
        """
        return self.create(request, *args, **kwargs)


class FarmDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FarmSerializer
    lookup_url_kwarg = "slug"

    def get_object(self):
        slug = self.kwargs['slug']
        qs = Farm.objects.select_related("owner").get(slug=slug)
        return qs


class ProduceListingCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProduceListingSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        qs = ProduceListing.objects.select_related("owner") \
            .filter(owner=self.request.user)
        return qs

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProduceListingDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProduceListingSerializer
    lookup_url_kwarg = "uid"

    def get_object(self):
        uid = self.kwargs['uid']
        qs = ProduceListing.objects.select_related("owner").get(uid=uid)
        return qs
