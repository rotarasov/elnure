import pytest


pytestmark = pytest.mark.django_db


def test_create_user(user_model):
    user = user_model.objects.create_user(
        email="student@nure.ua",
        password="student_password",
        first_name="Андрей",
        last_name="Васильев",
        patronymic="Олегович",
    )

    assert user.email == "student@nure.ua"
    assert user.password != "student_password"
    assert user.first_name == "Андрей"
    assert user.last_name == "Васильев"
    assert user.patronymic == "Олегович"
    assert user.academic_group == None


@pytest.mark.usefixtures("roles")
def test_create_superuser(user_model):
    superuser = user_model.objects.create_superuser(
        email="admin@nure.ua",
        password="admin_password",
        first_name="Евгений",
        last_name="Кондратюк",
        patronymic="Романович",
    )

    assert superuser.roles.count() == 1
    assert superuser.roles.first().name == "Administrator"
