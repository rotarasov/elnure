from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

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
