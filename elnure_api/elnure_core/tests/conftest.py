from pytest_factoryboy import register

from elnure_core.tests import factories


register(factories.InstructorFactory)
register(factories.BlockFactory)
register(factories.ElectiveCourseFactory)
register(factories.InstructorAssignmentFactory)
