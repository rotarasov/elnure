from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from elnure_api.admin import elnure_admin_site
from elnure_common.admin import forms as common_forms
from elnure_core import models as core_models
from elnure_core.admin import forms as core_forms
from elnure_users import models


class ElectiveGroupInlineAdmin(admin.TabularInline):
    form = core_forms.ElectiveGroupStudentAssociationInlineForm
    model = core_models.ElectiveGroupStudentAssociation
    fields = ["elective_group", "choice"]
    extra = 1
    verbose_name = _("Elective group")
    verbose_name_plural = _("Elective groups")


class ChoiceInlineAdmin(admin.StackedInline):
    model = core_models.Choice
    fields = ["semester", "value", "application_window", "strategy"]
    extra = 1


@admin.register(models.User, site=elnure_admin_site)
class UserAdmin(admin.ModelAdmin):
    fields = [
        "active",
        "email",
        "password",
        "first_name",
        "last_name",
        "patronymic",
        "academic_group",
        "is_admin",
    ]
    inlines = [ElectiveGroupInlineAdmin, ChoiceInlineAdmin]


class StudentInlineAdmin(admin.TabularInline):
    fields = [
        "email",
        "first_name",
        "last_name",
        "patronymic",
    ]
    model = models.Student
    extra = 0

    # Enforce all changes to be made on student page

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj):
        return False


@admin.register(models.AcademicGroup, site=elnure_admin_site)
class AcademicGroupAdmin(admin.ModelAdmin):
    form = common_forms.StudentGroupForm
    fields = ["name"]
    inlines = [StudentInlineAdmin]
