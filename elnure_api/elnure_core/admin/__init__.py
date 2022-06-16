from django.contrib import admin, messages
from django.db import models as django_models
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_json_widget.widgets import JSONEditorWidget

from docio.writers.excel.run_snapshot_writer import RunSnapshptWriter
from elnure_api.admin import elnure_admin_site
from elnure_common.admin import forms as common_forms
from elnure_core import models
from elnure_core.admin import forms
from elnure_core.strategies import make_run_snapshot_permanent, StrategyError


@admin.register(models.Instructor, site=elnure_admin_site)
class InstructorAdmin(admin.ModelAdmin):
    readonly_fields = ["id"]
    fields = ["id", "full_name"]


@admin.register(models.Block, site=elnure_admin_site)
class BlockAdmin(admin.ModelAdmin):
    form = forms.BlockForm
    readonly_fields = ["id"]
    fields = [
        "id",
        "name",
        "total_credits",
        "capacity",
        "semester",
        "must_choose",
        "elective_courses",
    ]
    list_display = ["name", "total_credits", "semester"]
    ordering = ["semester_id"]


class InstructorInlineAdmin(admin.TabularInline):
    model = models.InstructorAssignment
    fields = ["instructor", "position"]
    extra = 1
    fk_name = "to_elective_course"


@admin.register(models.ElectiveCourse, site=elnure_admin_site)
class ElectiveCourseAdmin(admin.ModelAdmin):
    readonly_fields = ["block"]
    readonly_fields = ["id"]
    fields = [
        "id",
        "name",
        "shortcut",
        "syllabus",
        "capacity",
        "credits",
        "block",
        "performance_assessment",
    ]
    inlines = [InstructorInlineAdmin]
    list_display = ["name", "shortcut", "block", "semester"]
    ordering = ["block__semester_id", "name"]
    search_fields = ["name", "shortcut", "semester"]

    @admin.display(ordering="block__semester_id")
    def semester(self, obj):
        return obj.block.semester_id if obj.block else None


class StudentInlineAdmin(admin.TabularInline):
    form = forms.ElectiveGroupStudentAssociationInlineForm
    model = models.ElectiveGroupStudentAssociation
    fields = ["student", "choice"]
    extra = 1
    verbose_name = _("Student")
    verbose_name_plural = _("Students")


@admin.register(models.ElectiveGroup, site=elnure_admin_site)
class ElectiveGroupAdmin(admin.ModelAdmin):
    form = common_forms.StudentGroupForm
    readonly_fields = ["id"]
    fields = ["id", "name", "elective_course"]
    list_display = ["name", "elective_course"]
    search_fields = ["name", "elective_course"]
    inlines = [StudentInlineAdmin]


@admin.register(models.RunSnapshot, site=elnure_admin_site)
class RunSnapshotAdmin(admin.ModelAdmin):
    form = forms.RunSnapshotForm
    readonly_fields = ["id", "strategy"]
    fields = [
        "id",
        "application_window",
        "strategy",
        "need_redistribution",
        "result",
        "status",
    ]

    list_display = ["application_window", "strategy", "status"]
    ordering = ["-application_window__update_date", "-update_date"]

    formfield_overrides = {
        django_models.JSONField: {
            "widget": JSONEditorWidget(width="70%", height="350px")
        },
    }

    def response_change(self, request, obj):
        response = super().response_change(request, obj)

        if "_save_and_make_permanent" in request.POST:
            try:
                make_run_snapshot_permanent(obj)
            except StrategyError as exc:
                self.message_user(
                    request, f"Permanent save error: {str(exc)}", messages.ERROR
                )

                opts = self.model._meta
                redirect_url = reverse(
                    f"admin:{opts.app_label}_{opts.model_name}_change",
                    args=(obj.pk,),
                    current_app=self.admin_site.name,
                )

                return HttpResponseRedirect(redirect_url)

            self.message_user(
                request,
                f"Elective groups are generated for application window: {str(obj.application_window)}",
            )

        if "_save_and_export" in request.POST:
            writer = RunSnapshptWriter()
            stream = writer.build(obj)

            response = HttpResponse(
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            response.headers[
                "Content-Disposition"
            ] = f"attachment; filename={str(obj.application_window)}.xlsx"
            response.write(stream)

        return response
