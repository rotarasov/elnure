from django_filters import rest_framework as filters

from elnure_core import models


class ElectiveCourseFilterSet(filters.FilterSet):
    semestr = filters.NumberFilter(field_name="semester", lookup_expr="exact")
    semester__gte = filters.NumberFilter(field_name="semester", lookup_expr="gte")
    semester__lte = filters.NumberFilter(field_name="semester", lookup_expr="lte")
    semester__gt = filters.NumberFilter(field_name="semester", lookup_expr="gt")
    semester__lt = filters.NumberFilter(field_name="semester", lookup_expr="lt")

    instructors__contains = filters.ModelMultipleChoiceFilter(
        queryset=models.Instructor.objects.all(),
        field_name="instructors__id",
        to_field_name="id",
        conjoined=True,
    )

    class Meta:
        model = models.ElectiveCourse
        fields = ["semester", "instructors", "block"]
