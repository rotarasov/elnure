import factory

from elnure_common.tests.factories import fields as custom_fields
from elnure_users import models


class AcademicGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.AcademicGroup


class StudentFactory(factory.django.DjangoModelFactory):
    email = factory.Sequence(lambda n: f"student{n}@nure.ua")
    first_name = custom_fields.FuzzyFirstName()
    last_name = custom_fields.FuzzyLastName()
    patronymic = custom_fields.FuzzyPatronymicName()
    academic_group = factory.SubFactory(AcademicGroupFactory)
    is_admin = False

    class Meta:
        model = models.User
