from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class AuditMixin:
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


class ActiveMixin:
    active = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1)], default=1
    )


class CommonModel(AuditMixin, ActiveMixin, models.Model):
    class Meta:
        abstract = True
