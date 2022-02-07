import pytest
from django.apps import apps
from django.conf import settings

from elnure_users.models import Role


@pytest.fixture
def roles():
    return {
        "Administrator": Role.objects.create(
            name="Administrator", description="lorem ipsum"
        ),
        "Student": Role.objects.create(name="Student", description="lorem ipsum"),
    }


@pytest.fixture
def user_model():
    return apps.get_model(settings.AUTH_USER_MODEL)
