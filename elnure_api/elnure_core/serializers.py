from xml.dom import ValidationErr
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from elnure_config import models as config_models
from elnure_config import serializers as config_serializers
from elnure_core import models
from elnure_common.serializers import ReadOnlyModelSerializer
from elnure_users.serializers import UserSerializer


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ["create_date", "update_date"]
        model = models.Instructor


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ["create_date", "update_date"]
        model = models.Block


class InstructorAssignmentSerializer(serializers.ModelSerializer):
    instructor_id = serializers.IntegerField()
    full_name = serializers.CharField(source="instructor.full_name", read_only=True)

    class Meta:
        fields = ["instructor_id", "full_name", "position"]
        model = models.InstructorAssignment


class ElectiveCourseSerializer(serializers.ModelSerializer):
    instructor_assignments = InstructorAssignmentSerializer(
        many=True, source="instructors.through.objects"
    )

    class Meta:
        fields = [
            "id",
            "instructor_assignments",
            "semester",
            "name",
            "shortcut",
            "syllabus",
            "capacity",
            "credits",
            "performance_assessment",
            "block",
        ]
        model = models.ElectiveCourse

    @transaction.atomic
    def create(self, validated_data):
        instructor_assignments = (
            validated_data.pop("instructors", {}).get("through", {}).get("objects", [])
        )

        instance = super().create(validated_data)

        self._save_instructor_assignments(instance, instructor_assignments)

        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        instructor_assignments = (
            validated_data.pop("instructors", {}).get("through", {}).get("objects", [])
        )

        instance = super().update(instance, validated_data)

        if instructor_assignments or not self.partial:
            self._save_instructor_assignments(instance, instructor_assignments)

        return instance

    @staticmethod
    def _save_instructor_assignments(course, assignments):
        models.InstructorAssignment.objects.filter(to_elective_course=course).delete()

        objs = [
            models.InstructorAssignment(to_elective_course=course, **ia)
            for ia in assignments
        ]
        models.InstructorAssignment.objects.bulk_create(objs)


class ChoiceSerializer(serializers.ModelSerializer):
    value = serializers.JSONField(required=True)
    application_window = serializers.PrimaryKeyRelatedField(
        allow_null=False,  # Disabling null values
        queryset=config_models.ApplicationWindow.objects.all(),
    )

    def validate(self, attrs):
        application_window = attrs.get("application_window")
        now = timezone.now()
        if application_window and application_window.start_date > now:
            raise serializers.ValidationError(
                f"Students can not make a choice earlier than start date of the application window."
            )
        if application_window and application_window.end_date < now:
            raise serializers.ValidationError(
                f"Students can not make a choice later than start date of the application window."
            )

        return attrs

    def validate_value(self, value):
        if not value:
            raise serializers.ValidationError("Value should not be empty object.")
        return value

    class Meta:
        exclude = ["create_date", "update_date", "elective_groups"]
        model = models.Choice
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=models.Choice.objects.all(),
                fields=["student", "application_window"],
                message="Only one application is allowed for the current application window.",  # Overriding django default message
            )
        ]


class ElectiveGroup(serializers.ModelSerializer):
    class Meta:
        exclude = ["create_date", "update_date"]
        model = models.ElectiveGroup


class RefChoiceSerializer(ReadOnlyModelSerializer):
    student = UserSerializer()
    elective_groups = ElectiveGroup(many=True, allow_empty=True)
    application_window = config_serializers.ApplicationWindowSerializer()

    class Meta:
        exclude = ["create_date", "update_date"]
        model = models.Choice
