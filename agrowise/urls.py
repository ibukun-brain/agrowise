from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from home.views import RedirectSocial

urlpatterns = [
    path("api/", include("home.api.urls", namespace="home")),
    path("api/", include("farms.api.urls", namespace="farms")),
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.jwt")),
    path("api/oauth/", include("djoser.social.urls")),
    path("accounts/profile/", RedirectSocial.as_view()),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-docs",
    ),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    extrapatterns = [path("__debug__/", include("debug_toolbar.urls"))]
    urlpatterns += extrapatterns
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
