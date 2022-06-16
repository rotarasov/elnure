from constance import config
from rest_framework import serializers

from elnure_common.serializers import ReadOnlyModelSerializer
from elnure_config import models


class ApplicationWindowSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ["create_date", "update_date"]
        model = models.ApplicationWindow


class RefApplicationWindowSerializer(ReadOnlyModelSerializer):
    semesters = serializers.SerializerMethodField()

    def get_semesters(self, obj):
        return config.SEMESTERS

    class Meta:
        exclude = ["create_date", "update_date"]
        model = models.ApplicationWindow
