from django.contrib.admin.apps import AdminConfig


class ElnureAdminConfig(AdminConfig):
    default_site = "elnure_api.admin.ElnureAdminSite"
