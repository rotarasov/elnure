from django_filters import rest_framework as filters

from elnure_core import models


class ElectiveCourseFilterSet(filters.FilterSet):
    instructors__contains = filters.ModelMultipleChoiceFilter(
        queryset=models.Instructor.objects.all(),
        field_name="instructors__id",
        to_field_name="id",
        conjoined=True,
    )

    class Meta:
        model = models.ElectiveCourse
        fields = ["instructors", "block"]


class ChoiceFilterSet(filters.FilterSet):
    application_window = filters.NumberFilter(
        field_name="application_window_id", lookup_expr="exact"
    )
