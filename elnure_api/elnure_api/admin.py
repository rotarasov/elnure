from django.conf import settings
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class ElnureAdminSite(admin.AdminSite):
    site_title = _("Elnure Admin Panel")
    site_header = _("Elnure Admin")

    def login(self, request, extra_context=None):
        google_auth_context = {
            "GOOGLE_OAUTH2_CLIENT_ID": settings.GOOGLE_OAUTH2_CLIENT_ID,
            "BASE_BACKEND_URL": settings.BASE_BACKEND_URL,
        }
        extra_context = extra_context or {}
        return super().login(request, {**extra_context, **google_auth_context})
