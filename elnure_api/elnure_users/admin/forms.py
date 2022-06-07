from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from elnure_users import models

# TODO: Possibly replace this with the formats mapping from excel lib
ALLOWED_CONTENT_TYPES = [
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
]


class ImportUserMappingForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        file = self.cleaned_data["file"]

        if file.content_type not in ALLOWED_CONTENT_TYPES:
            raise ValidationError(_("User mapping file should be .xls/.xlsx format."))


class UserForm(forms.ModelForm):
    changed_password = forms.BooleanField(label=_("Changed password?"), required=False)

    def clean(self):
        changed_password = self.cleaned_data.pop("changed_password", False)
        is_admin = self.cleaned_data["is_admin"]
        academic_group = self.cleaned_data["academic_group"]

        if changed_password:
            self.instance.set_password(self.instance.password)

        if is_admin and academic_group:
            raise ValidationError(_("Admin can not be assigned to academic group"))
