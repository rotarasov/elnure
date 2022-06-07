from constance.admin import Config, ConstanceAdmin
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from elnure_api.admin import elnure_admin_site
from elnure_config import models
from elnure_config.admin import forms
from elnure_core.strategies import run_strategy, StrategyError


@admin.register(models.Semester, site=elnure_admin_site)
class SemesterAdmin(admin.ModelAdmin):
    ordering = ["id"]
    exclude = ["study_year"]
    form = forms.SemesterForm


@admin.register(models.ApplicationWindow, site=elnure_admin_site)
class ApplicationWindowAdmin(admin.ModelAdmin):
    readonly_fields = ["id"]
    fields = ["id", "start_date", "end_date"]
    ordering = ["-start_date"]

    def response_change(self, request, obj):
        response = super().response_change(request, obj)

        if "_save_and_run" in request.POST:
            try:
                run_strategy(obj)
            except StrategyError as exc:
                self.message_user(
                    request, f"Algorithm error: {str(exc)}", messages.ERROR
                )

                opts = self.model._meta
                redirect_url = reverse(
                    f"admin:{opts.app_label}_{opts.model_name}_change",
                    args=(obj.pk,),
                    current_app=self.admin_site.name,
                )

                return HttpResponseRedirect(redirect_url)

        return response


elnure_admin_site.register([Config], admin_class=ConstanceAdmin)
