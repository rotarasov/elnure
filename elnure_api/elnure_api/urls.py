from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from elnure_api.admin import elnure_admin_site


urlpatterns = [
    path("admin/", elnure_admin_site.urls),
    path("api/v1/", include("elnure_core.urls")),
    path("api/v1/", include("elnure_users.urls")),
    path("api/v1/", include("elnure_config.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
