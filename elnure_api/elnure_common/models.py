from datetime import datetime

from django.core.validators import MaxValueValidator
from django.db import models


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

    class Meta:
        abstract = True
