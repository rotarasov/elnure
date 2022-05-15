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
    class Meta:
        exclude = ["create_date", "update_date"]
        model = models.InstructorAssignment


class ElectiveCourseSerializer(serializers.ModelSerializer):
    instructor_assignments = InstructorAssignmentSerializer(
        many=True, source="instructors.through.objects"
    )

    class Meta:
        fields = "__all__"
        model = models.ElectiveCourse

    def create(self, validated_data):
        instructor_assignments = validated_data.pop("instructor_assignments", [])

        instance = super().create(validated_data)

        self._save_instructor_assignments(instance, instructor_assignments)

        return instance

    def update(self, instance, validated_data):
        instructor_assignments = validated_data.pop("instructor_assignments", [])

        instance = super().update(instance, validated_data)

        self._save_instructor_assignments(instance, instructor_assignments)

        return instance

    def _save_instructor_assignments(course, assignments):
        models.InstructorAssignment.filter(to_elective_course=course).delete()

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
