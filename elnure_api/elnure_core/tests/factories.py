import factory
from factory import fuzzy

from elnure_common.tests.factories import fields as custom_fields
from elnure_core import models


class InstructorFactory(factory.django.DjangoModelFactory):
    full_name = custom_fields.FuzzyFullName()

    class Meta:
        model = models.Instructor


class BlockFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"block{n}")

    class Meta:
        model = models.Block


class ElectiveCourseFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"course{n}")
    shortcut = factory.Sequence(lambda n: f"crs{n}")
    syllabus = factory.Sequence(lambda n: f"https://storage-provider.com/crs{n}")
    credits = fuzzy.FuzzyInteger(3, 5)
    performance_assessment = models.ElectiveCourse.PerformanceAssessment.GRADED_SEMESTER
    block = factory.SubFactory(BlockFactory)

    class Meta:
        model = models.ElectiveCourse


class InstructorAssignmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.InstructorAssignment


class ChoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Choice
