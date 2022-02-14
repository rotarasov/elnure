import enum

from django.db import models


class ElnureEnumField(models.CharField):
    def __init__(self, choices: models.Choices | list[tuple[str, str]], **options):
        if isinstance(choices, models.enums.ChoicesMeta):
            options.setdefault("max_length", len(max(choices.values, key=len)))
            options.setdefault("choices", choices.choices)
        else:
            options.setdefault("choices", choices)
        super().__init__(**options)
