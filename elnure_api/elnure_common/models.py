from datetime import datetime
from functools import cache

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from utils import get_current_study_year_by_start_year


class AuditMixin(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ActiveMixin(models.Model):
    active = models.PositiveIntegerField(validators=[MaxValueValidator(1)], default=1)

    class Meta:
        abstract = True


class CommonModel(AuditMixin, models.Model):
    class Meta:
        abstract = True


class StudentGroupMixin(models.Model):
    name = models.CharField(max_length=30)
    start_year = models.PositiveIntegerField(
        help_text="Year when student group was formed",
    )

    @cache
    def _get_splitted_group(self):
        """
        SE-18-5 => ("SE", "18", "5")
        """
        return self.name.split("-")

    @property
    def start_year(self):
        # TODO: Move this logic to django form for student group creation
        row_year = int(self._get_splitted_group()[1])
        return datetime.strptime("%y", row_year).year

    @property
    def current_study_year(self):
        return get_current_study_year_by_start_year(self.start_year)

    @property
    def number(self):
        return int(self._get_splitted_group()[2])

    class Meta:
        abstract = True
