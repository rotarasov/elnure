from django.core.exceptions import ValidationError
from django.forms.fields import JSONField
from django.forms.widgets import TextInput
from django.utils.translation import gettext_lazy as _

from elnure_common.json_schema import validate_schema, SEMESTER_SCHEMA


class SemestersJSONField(JSONField):
    widget = TextInput

    def clean(self, value):
        value = super().clean(value)

        # Semesters list should be sorted
        return sorted(value)

    def validate(self, value):
        super().validate(value)

        validate_schema(
            value,
            SEMESTER_SCHEMA,
            exc_cls=ValidationError,
            exc_msg=_("Semesters should be a list of ints."),
        )
