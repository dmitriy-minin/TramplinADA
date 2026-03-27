from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from apps.core.views import HomeView, healthcheck
from apps.accounts.views import dashboard_view, public_profile_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("api/health/", healthcheck, name="healthcheck"),
    path("auth/", include("apps.accounts.urls")),
    path("opportunities/", include("apps.opportunities.urls")),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("dashboard/applicant/", include("apps.accounts.applicant_urls", namespace="applicant")),
    path("dashboard/employer/", include("apps.opportunities.employer_urls", namespace="employer")),
    path("curator/", include("apps.curator.urls", namespace="curator")),
    path("api/", include("apps.opportunities.api_urls")),
    path("profile/<int:pk>/", public_profile_view, name="public_profile"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
