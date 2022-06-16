from constance import config
from django.core import serializers as django_serializer
from rest_framework import serializers

from elnure_common.serializers import ReadOnlyModelSerializer
from elnure_config import models


class ApplicationWindowSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ["create_date", "update_date"]
        model = models.ApplicationWindow


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ["create_date", "update_date"]
        model = models.Semester


class RefApplicationWindowSerializer(ReadOnlyModelSerializer):
    semesters = serializers.SerializerMethodField()

    def get_semesters(self, obj):
        return SemesterSerializer(
            models.Semester.objects.filter(id__in=config.SEMESTERS), many=True
        ).data

    class Meta:
        exclude = ["create_date", "update_date"]
        model = models.ApplicationWindow
