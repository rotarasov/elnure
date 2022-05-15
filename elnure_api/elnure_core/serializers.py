from django.db import transaction
from rest_framework import serializers

from elnure_core import models


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.Instructor


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
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


class ApplicationWindowSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.ApplicationWindow


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.Choice
