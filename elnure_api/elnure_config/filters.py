from datetime import datetime

from django.db.models import Q
from django_filters import rest_framework as filters

from elnure_config import models


# TODO: filter does not work
class ActiveApplicationWindowFilter(filters.BooleanFilter):
    def filter(self, qs, value):
        now = datetime.now()
        if value is True:
            return qs.filter(start_date__lte=now, end_date__gt=now)
        elif value is False:
            return qs.filter(Q(start_date__gt=now) | Q(end_date__lte=now))
        return qs


class ApplicationWindowFilterSet(filters.FilterSet):
    active = ActiveApplicationWindowFilter()
