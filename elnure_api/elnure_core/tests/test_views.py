import pytest

from django.urls import reverse

from elnure_core import models


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "query_params,expected_count",
    [
        ({"semester": 3}, 1),
        ({"semester__gt": 2}, 2),
        ({"semester__lt": 2}, 0),
        ({"instructors__contains": [1, 2]}, 1),
        ({"instructors__contains": [1]}, 2),
        ({"instructors__contains": [2]}, 1),
    ],
)
def test_elective_course_filtering(
    instructor_factory,
    elective_course_factory,
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
    ec2 = elective_course_factory(semester=4)
    ec2.instructors.add(
        i1, through_defaults={"position": models.InstructorAssignment.Position.LECTURER}
    )

    response = client.get(reverse("elective-course-list"), data=query_params)
    assert response.status_code == 200, response.json()
    assert len(response.data) == expected_count, response.json()
