import pytest

from django.urls import reverse

from elnure_core import models


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "query_params,expected_count",
    [
        ({"semester": 3}, 1),
        # ({"semester__gt": 2}, 2),
        # ({"semester__lt": 2}, 0),
        # ({"instructors": [1, 2]}, 1),
        # ({"instructors": [1]}, 0),
        # ({"instructors__contains": [1]}, 2),
        # ({"instructors__contains": [3]}, 0),
    ],
)
def test_elective_course_filtering(
    instructor_factory,
    elective_course_factory,
    instructor_assignment_factory,
    client,
    query_params,
    expected_count,
):
    i1 = instructor_factory()
    i2 = instructor_factory()
    ec1 = elective_course_factory(semester=3)
    ec1.instructors.add(
        i1, through_defaults={"position": models.InstructorAssignment.Position.LECTURER}
    )
    ec1.instructors.add(
        i2,
        through_defaults={"position": models.InstructorAssignment.Position.ASSISTANT},
    )
    # instructor_assignment_factory(
    #     to_elective_course=ec1,
    #     instructor=i1,
    #     position=models.InstructorAssignment.Position.LECTURER,
    # )
    # instructor_assignment_factory(
    #     to_elective_course=ec1,
    #     instructor=i2,
    #     position=models.InstructorAssignment.Position.ASSISTANT,
    # )
    ec2 = elective_course_factory(semester=4)
    ec2.instructors.add(
        i1, through_defaults={"position": models.InstructorAssignment.Position.LECTURER}
    )

    from elnure_api import urls
    from pprint import pprint

    pprint(urls.urlpatterns)
    response = client.get(reverse("elective-course-list"), data=query_params)
    assert response.status_code == 200
    assert len(response.data) == expected_count
