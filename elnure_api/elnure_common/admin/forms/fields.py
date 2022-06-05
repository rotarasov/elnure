from django.core.exceptions import ValidationError
from django.forms.fields import JSONField
from django.forms.widgets import TextInput
from django.utils.translation import gettext_lazy as _


class SemestersJSONField(JSONField):
    widget = TextInput

    def clean(self, value):
        value = super().clean(value)

        # Semesters list should be sorted
        return sorted(value)

    def validate(self, value):
        super().validate(value)

        if not isinstance(value, list) or not all(isinstance(s, int) for s in value):
            raise ValidationError(_("Semesters should be a list of ints."))
