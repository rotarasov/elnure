from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.translation import gettext_lazy as _


class ElnureAdminSite(admin.AdminSite):
    site_title = _("Elnure Admin Panel")
    site_header = _("Elnure Admin")

    def get_urls(self):
        urls = super().get_urls()

        def wrap_view(view):
            view = self.admin_view(view)
            view.admin_site = self
            return view

        custom_urls = [
            path(
                "elnure_users/import_user_mappings",
                wrap_view(self.import_user_mappings),
                name="import-user-mappings",
            ),
        ]

        return custom_urls + urls

    def login(self, request, extra_context=None):
        google_auth_context = {
            "GOOGLE_OAUTH2_CLIENT_ID": settings.GOOGLE_OAUTH2_CLIENT_ID,
            "BASE_BACKEND_URL": settings.BASE_BACKEND_URL,
        }
        extra_context = extra_context or {}
        return super().login(request, {**extra_context, **google_auth_context})

    def import_user_mappings(self, request, extra_context=None):
        from elnure_users.admin.forms import ImportUserMappingForm

        request.current_app = self.name

        context = {
            **self.each_context(request),
            "breadcrumb_node": _("Import user mappings"),
            "action": "Import user mappings",
            "action_class": "import-user-mappings",
        }
        context.update(extra_context or {})

        if request.method == "GET":
            form = ImportUserMappingForm()
            context.update(form.get_context())
            return TemplateResponse(request, "admin/import_form.html", context)

        form = ImportUserMappingForm(request.POST, request.FILES)
        if form.is_valid():
            print("Handle!!!")

        context.update(form.get_context())

        return TemplateResponse(request, "admin/import_form.html", context)


elnure_admin_site = ElnureAdminSite(name="elnure_admin")
