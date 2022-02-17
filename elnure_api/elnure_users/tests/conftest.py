import pytest
from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import Group


@pytest.fixture
def groups():
    return {
        "Administrator": Group.objects.create(name="Administrator"),
        "Student": Group.objects.create(name="Student"),
    }


@pytest.fixture
def user_model():
    return apps.get_model(settings.AUTH_USER_MODEL)
