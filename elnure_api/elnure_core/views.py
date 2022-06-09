from rest_framework.mixins import (
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    ListModelMixin,
)
from rest_framework.throttling import UserRateThrottle
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from elnure_core import serializers, models, filters


class InstructorViewSet(ModelViewSet):
    """
    Instructor view set

    retrieve: Get an instructor by given id
    list: Get all instructors
    create: Create an instrucor
    update: Update an instrucor by id
    partial_update: Update only some fields of an instrucor by id
    delete: Delete an instrucor by id
    """

    serializer_class = serializers.InstructorSerializer
    queryset = models.Instructor.objects


class BlockViewSet(ModelViewSet):
    """
    Block view set

    retrieve: Get a block by given id
    list: Get all blocks
    create: Create a block
    update: Update a block by id
    partial_update: Update only some fields of a block by id
    delete: Delete a block by id
    """

    serializer_class = serializers.BlockSerializer
    queryset = models.Block.objects


class ElectiveCourseViewSet(ModelViewSet):
    """
    Elective Course view set

    retrieve: Get an elective course by given id
    list: Get all elective courses or filtered by semester or study year
    create: Create an elective course
    update: Update an elective course by id
    partial_update: Update only some fields of an elective course by id
    delete: Delete an elective course by id
    """

    serializer_class = serializers.ElectiveCourseSerializer
    queryset = models.ElectiveCourse.objects
    filterset_class = filters.ElectiveCourseFilterSet


class ChoiceRateThrottle(UserRateThrottle):
    rate = "100/minute"


class ChoiceViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    """
    Student Choice view set

    retrieve: Get a student choice by given id
    list: Get all student choices or filtered by study year or year of application
    create: Create student choice
    update: Update student choice by id
    partial_update: Update only some fields of student choice by id
    """

    throttle_classes = [ChoiceRateThrottle]
    filterset_class = filters.ChoiceFilterSet

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return serializers.RefChoiceSerializer
        return serializers.ChoiceSerializer

    def get_queryset(self):
        return models.Choice.objects.select_related("application_window")
