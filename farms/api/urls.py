from django.urls import path

from farms.api.views import (
    FarmDetailAPIView,
    FarmListCreateAPIView,
    ProduceListingCreateAPIView,
    ProduceListingDetailAPIView,
)

app_name = "farms"

urlpatterns = [
    path(
        route="farms/",
        view=FarmListCreateAPIView.as_view(),
        name="farm-list"
    ),
    path(
        route="farms/<slug:slug>/",
        view=FarmDetailAPIView.as_view(),
        name="farm-detail"
    ),
    path(
        route="produce-listings/",
        view=ProduceListingCreateAPIView.as_view(),
        name="produce-listing"
    ),
    path(
        route="produce-listings/<uuid:uid>/",
        view=ProduceListingDetailAPIView.as_view(),
        name="produce-listing-detail"
    )
]
