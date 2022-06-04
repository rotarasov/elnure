from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from elnure_api.admin import elnure_admin_site
from elnure_common.admin import forms as common_forms
from elnure_core import models
from elnure_core.admin import forms


@admin.register(models.Instructor, site=elnure_admin_site)
class InstructorAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Block, site=elnure_admin_site)
class BlockAdmin(admin.ModelAdmin):
    form = forms.BlockForm
    fields = [
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


@admin.register(models.ElectiveCourse, site=elnure_admin_site)
class ElectiveCourseAdmin(admin.ModelAdmin):
    readonly_fields = ["block"]
    fields = [
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
    fields = ["name", "elective_course"]
    list_display = ["name", "elective_course"]
    search_fields = ["name", "elective_course"]
    inlines = [StudentInlineAdmin]


@admin.register(models.RunSnapshot, site=elnure_admin_site)
class RunSnapshotAdmin(admin.ModelAdmin):
    pass
