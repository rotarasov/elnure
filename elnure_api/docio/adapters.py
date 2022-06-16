from abc import ABCMeta

from constance import config
from django.utils.translation import gettext_lazy as _

from docio.models import Sheet
from elnure_core.models import (
    RunSnapshot,
    ElectiveCourse,
    ElectiveGroupStudentAssociation,
)


class AdapterError(Exception):
    pass


class BaseAdapter(metaclass=ABCMeta):
    def forward(self, from_data):
        raise NotImplementedError()

    def backward(self, to_data):
        raise NotImplementedError()


class RunSnapshotDictsAdapter(BaseAdapter):
    def forward(self, run_snapshot) -> list[Sheet]:
        result = []
        for semester_id in config.SEMESTERS:
            semester_key = f"Semester {semester_id}"
            sheet = Sheet(name=semester_key, data={})

            snapshot_data = run_snapshot.result[str(semester_id)]

            elective_courses = ElectiveCourse.objects.filter(
                id__in=[int(_id) for _id in snapshot_data.keys()]
            ).in_bulk()

            for elective_course_id, elective_groups in snapshot_data.items():
                elective_course = elective_courses[int(elective_course_id)]

                elective_course_key = (
                    f"{elective_course.name}({elective_course.shortcut})"
                )
                sheet.data[elective_course_key] = {}

                for student_group_association in (
                    ElectiveGroupStudentAssociation.objects.filter(
                        elective_group__name__in=elective_groups.keys()
                    )
                    .order_by(
                        "student__last_name",
                        "student__first_name",
                        "student__patronymic",
                    )
                    .select_related("elective_group", "student__academic_group")
                ):
                    elective_group_key = student_group_association.elective_group.name
                    if not elective_group_key in sheet.data[elective_course_key]:
                        sheet.data[elective_course_key][elective_group_key] = []

                    student = student_group_association.student
                    sheet.data[elective_course_key][elective_group_key].append(
                        [
                            f"{len(sheet.data[elective_course_key][elective_group_key]) + 1}.",
                            student.email,
                            student.get_full_name(),
                            student.academic_group.name,
                        ]
                    )

            result.append(sheet)

        return result
