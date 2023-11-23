from django.urls import path

from home.api import views as home_api_view

app_name = "home"

urlpatterns = [
    path(route="openapi/", view=home_api_view.OpenAPIView.as_view(), name="openapi"),
]
