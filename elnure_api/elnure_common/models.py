from datetime import datetime
from functools import cache

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class AuditMixin(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ActiveMixin(models.Model):
    active = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1)], default=1
    )

    class Meta:
        abstract = True


class CommonModel(AuditMixin, models.Model):
    class Meta:
        abstract = True


class StudyYear(models.IntegerChoices):
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4


class StudentGroupMixin(models.Model):
    name = models.CharField(max_length=30)

    @cache
    def _get_splitted_group(self):
        """
        SE-18-5 => ("SE", "18", "5")
        """
        return self.name.split("-")

    @property
    def start_year(self):
        """Year when student group was formed.
        First part states for department
        Second part states for start year
        Third part states for group number
        ex. SE-18-5 => 2018
        """
        row_year = int(self._get_splitted_group()[1])
        return datetime.strptime("%y", row_year)

    @property
    def current_study_year(self):
        """
        Can be obtained from the start year of the group
        NOTE: It is important to pay attention to the season of the year
        e.g. Group: SE-19-5
        Season: spring 2022 => StudyYear.THIRD
        Season: autumn 2022 => StudyYear.FOURTH
        """
        current_date = datetime.now()
        next_year = (
            current_date.month // 9
        )  # July and August are also considered as previous year
        return current_date.year - self.start_year + next_year

    @property
    def number(self):
        return int(self._get_splitted_group()[2])

    class Meta:
        abstract = True


class SemesterMixin(models.Model):
    semester = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(8)]
    )

    @property
    def study_year(self):
        """The study year for semester
        1, 2 => StudyYear.FIRST
        3, 4 => StudyYear.SECOND
        ...
        """
        return (self.semester + 1) // 2

    class Meta:
        abstract = True
