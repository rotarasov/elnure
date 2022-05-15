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


def test_create_elective_course(instructor_factory, client):
    instructor_factory()
    instructor_factory()
    data = {
        "instructor_assignments": [
            {"instructor_id": 1, "position": "LECTURER"},
            {"instructor_id": 2, "position": "ASSISTANT"},
        ],
        "semester": 2,
        "name": "Some test course",
        "shortcut": "SC1",
        "syllabus": "https://s3.syllabus.com",
        "credits": 5,
        "performance_assessment": "SESSION_EXAMINATION",
    }
    response = client.post(reverse("elective-course-list"), data=data)
    assert response.status_code == 201, response.json()

    obj = models.ElectiveCourse.objects.get(id=response.data["id"])
    assert obj.semester == response.data["semester"]
    assert obj.instructors.count() == 2


def test_update_elective_course(
    instructor_factory,
    elective_course_factory,
    client,
):
    i1 = instructor_factory()
    i2 = instructor_factory()
    ec1 = elective_course_factory(semester=3)
    ec1.instructors.add(
        i1, through_defaults={"position": models.InstructorAssignment.Position.LECTURER}
    )
    data = {
        "instructor_assignments": [
            {"instructor_id": i2.id, "position": "LECTURER"},
        ],
        "semester": ec1.semester,
        "name": ec1.name,
        "shortcut": ec1.shortcut,
        "syllabus": ec1.syllabus,
        "credits": ec1.credits,
        "performance_assessment": ec1.performance_assessment,
    }

    response = client.put(reverse("elective-course-detail", args=[ec1.id]), data=data)
    assert response.status_code == 200, response.json()

    assert ec1.instructors.first().id == i2.id

    i3 = instructor_factory()
    patch_data = {
        "instructor_assignments": [
            {"instructor_id": i3.id, "position": "LECTURER"},
        ],
    }
    response = client.patch(
        reverse("elective-course-detail", args=[ec1.id]), data=patch_data
    )
    assert response.status_code == 200, response.json()

    assert ec1.instructors.first().id == i3.id


def test_patch_not_delete_instructor_assignments(
    instructor_factory,
    elective_course_factory,
    client,
):
    i1 = instructor_factory()
    ec1 = elective_course_factory(semester=3)
    ec1.instructors.add(
        i1, through_defaults={"position": models.InstructorAssignment.Position.LECTURER}
    )

    response = client.patch(
        reverse("elective-course-detail", args=[ec1.id]), data={"semester": 4}
    )
    assert response.status_code == 200, response.json()

    assert ec1.instructors.count() == 1
    assert response.data["semester"] == 4
