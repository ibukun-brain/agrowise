from django.urls import path

from home.api import views as home_api_view

app_name = "home"

urlpatterns = [
    path(route="openapi/", view=home_api_view.OpenAPIView.as_view(), name="openapi"),
    path(
        route="openapi/history/",
        view=home_api_view.OpenAIHistoryListView.as_view(),
        name="openapi-history"
    ),
    path(
        route="openapi/history/<uuid:uid>/",
        view=home_api_view.OpenAIHistoryDetailView.as_view(),
        name="openapi-history-detail"
    ),
    path(
        "weather-forecast/",
        view=home_api_view.WeatherForecastAPIView.as_view(),
        name="weather-forecast",
    ),
]
