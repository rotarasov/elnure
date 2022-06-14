import factory

from elnure_config import models


class SemesterFactory(factory.django.DjangoModelFactory):
    id = 3
    total_credits = 5
    study_year = 2018

    class Meta:
        model = models.Semester


class ApplicationWindowFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ApplicationWindow
