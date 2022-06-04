from constance.admin import Config, ConstanceAdmin
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from elnure_api.admin import elnure_admin_site
from elnure_config import models
from elnure_config.admin import forms


@admin.register(models.Semester, site=elnure_admin_site)
class SemesterAdmin(admin.ModelAdmin):
    ordering = ["id"]
    exclude = ["study_year"]
    form = forms.SemesterForm


@admin.register(models.ApplicationWindow, site=elnure_admin_site)
class ApplicationWindowAdmin(admin.ModelAdmin):
    ordering = ["-start_date"]


elnure_admin_site.register([Config], admin_class=ConstanceAdmin)
