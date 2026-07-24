from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    path("api/auth/", include("apps.core.urls.auth_urls")),
    path("api/crm/", include("apps.core.urls.crm_urls")),
    path("api/hrm/", include("apps.core.urls.hrm_urls")),
    path("api/projects/", include("apps.core.urls.project_urls")),
    path("api/tickets/", include("apps.core.urls.ticket_urls")),
    path("api/notifications/", include("apps.core.urls.notification_urls")),
    path("api/security/", include("apps.core.urls.security_urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
