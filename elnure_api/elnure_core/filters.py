from django_filters import rest_framework as filters

from elnure_core import models


class ElectiveCourseFilterSet(filters.FilterSet):
    semester__gte = filters.NumberFilter(field_name="semester", lookup_expr="gte")
    semester__lte = filters.NumberFilter(field_name="semester", lookup_expr="lte")
    semester__gt = filters.NumberFilter(field_name="semester", lookup_expr="gt")
    semester__lt = filters.NumberFilter(field_name="semester", lookup_expr="lt")

    # test it
    instructors__contains = filters.ModelMultipleChoiceFilter(
        queryset=models.Instructor.objects,
        field_name="instructors",
        lookup_expr="contains",
    )

    class Meta:
        model = models.ElectiveCourse
        fields = ["semester", "instructors", "block"]
