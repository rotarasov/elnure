import pytest
from rest_framework.test import APIClient
from pytest_factoryboy import register

from elnure_core.tests import factories as core_factories
from elnure_users.tests import factories as user_factories
from elnure_config.tests import factories as config_factories


register(core_factories.InstructorFactory)
register(core_factories.BlockFactory)
register(core_factories.ElectiveCourseFactory)
register(core_factories.InstructorAssignmentFactory)
register(core_factories.ChoiceFactory)

register(user_factories.AcademicGroupFactory)
register(user_factories.StudentFactory)

register(config_factories.SemesterFactory)
register(config_factories.ApplicationWindowFactory)


@pytest.fixture
def client():
    client = APIClient()
    client.default_format = "json"
    return client
