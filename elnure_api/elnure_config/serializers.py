from rest_framework import serializers

from elnure_config import models


class ApplicationWindowSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ["create_date", "update_date"]
        model = models.ApplicationWindow
