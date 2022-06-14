import json
import pytest
from constance.test import override_config
from datetime import datetime, timedelta
from django.test.utils import override_settings

from elnure_core.strategies import run_strategy
from utils import get_start_year_by_current_study_year, shorten_year

pytestmark = pytest.mark.django_db


@override_config(
    SEMESTERS=[3],
    STRATEGY="DEFAULT",
    MAX_NUMBER_OF_STUDENTS_IN_ELECTIVE_GROUP=4,
    MIN_NUMBER_OF_STUDENTS_IN_ELECTIVE_GROUP=1,
    MAX_NUMBER_OF_ELECTIVE_GROUPS=5,
)
def test_strategy_successfully_distributed(
    student_factory,
    academic_group_factory,
    application_window_factory,
    block_factory,
    elective_course_factory,
    semester_factory,
    choice_factory,
):
    long_start_year = get_start_year_by_current_study_year(1)
    short_start_year = shorten_year(long_start_year)
    academic_group1 = academic_group_factory(
        name=f"ПЗПІ-{short_start_year}-1", start_year=long_start_year
    )
    academic_group2 = academic_group_factory(
        name=f"ПЗПІ-{short_start_year}-2", start_year=long_start_year
    )

    student1 = student_factory(academic_group=academic_group1, last_name="Аааааа")
    student2 = student_factory(academic_group=academic_group1, last_name="Бббббб")
    student3 = student_factory(academic_group=academic_group1, last_name="Вввввв")
    student4 = student_factory(academic_group=academic_group2, last_name="Гггггг")
    student5 = student_factory(academic_group=academic_group2, last_name="Дддддд")

    application_window = application_window_factory(
        start_date=datetime.now(), end_date=datetime.now() + timedelta(days=1)
    )

    semester3 = semester_factory(id=3, total_credits=5, study_year=1)

    block = block_factory(total_credits=5, must_choose=1, semester=semester3)

    elective_course1 = elective_course_factory(shortcut="CRS1", block=block)
    elective_course2 = elective_course_factory(shortcut="CRS2", block=block)

    choice_factory(
        student=student1,
        application_window=application_window,
        semester=semester3,
        value=[{"block_id": block.id, "elective_course_ids": [elective_course1.id]}],
    )
    choice_factory(
        student=student2,
        application_window=application_window,
        semester=semester3,
        value=[{"block_id": block.id, "elective_course_ids": [elective_course1.id]}],
    )
    choice_factory(
        student=student3,
        application_window=application_window,
        semester=semester3,
        value=[{"block_id": block.id, "elective_course_ids": [elective_course1.id]}],
    )
    choice_factory(
        student=student4,
        application_window=application_window,
        semester=semester3,
        value=[{"block_id": block.id, "elective_course_ids": [elective_course2.id]}],
    )
    choice_factory(
        student=student5,
        application_window=application_window,
        semester=semester3,
        value=[{"block_id": block.id, "elective_course_ids": [elective_course2.id]}],
    )

    run_snapshot = run_strategy(application_window)

    assert run_snapshot.need_redistribution == {3: []}
    assert run_snapshot.result == {
        3: {
            elective_course1.id: {
                f"ПЗПІ[CRS1]-{short_start_year}-1": [
                    {"email": student1.email, "academic_group": academic_group1.name},
                    {"email": student2.email, "academic_group": academic_group1.name},
                    {"email": student3.email, "academic_group": academic_group1.name},
                ]
            },
            elective_course2.id: {
                f"ПЗПІ[CRS2]-{short_start_year}-1": [
                    {"email": student4.email, "academic_group": academic_group2.name},
                    {"email": student5.email, "academic_group": academic_group2.name},
                ]
            },
        }
    }
