from collections import defaultdict

from constance import config
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from elnure_common.json_schema import (
    validate_schema,
    DefaultStrategySchemas,
)
from elnure_config.models import Semester, ApplicationWindow
from elnure_core.models import (
    ElectiveCourse,
    ElectiveGroup,
    ElectiveGroupStudentAssociation,
    Strategy,
    RunSnapshot,
)
from elnure_core.strategies.base import BaseChoiceStrategy, StrategyError
from elnure_users.models import Student
from utils import (
    ElectiveGroupNameFactory,
    get_start_year_by_current_study_year,
    get_study_years_by_semesters,
    get_start_year_by_group_name,
    shorten_year,
)


class ErrorMessage:
    invalid_semesters_num = _(
        "Number of semester configs should be equal to {num_of_semesters}."
    )
    no_semester_config = _("{semester} semester does not have SemesterConfig.")


class RedistributeReason:
    demounted_elective_course = "demounted_elective_course"
    choiceless_students = "choiceless_students"


class DefaultChoiceStrategy(BaseChoiceStrategy):
    """
    Default choice strategy aims to form elective groups by the update_date of the choice.
    The student who earlier applied will be able to get to elective courses w/ restricted capacity.

    Choice value is assumed to have the following structure
    >>> value = [
    ...     {"block_id": <block_id:int>, "elective_course_ids": [<elective_course_id:int>, ...]},
    ...     {"block_id": <block_id:int>, "elective_course_ids": [<elective_course_id:int>, ...]},
    ... ]
    Generated snapshot result will have the following structure:
    >>> {
    ...    "<elective_course_id>": {
    ...        "<elective_group_name 1>": [
    ...            <Student aneksin.vasil@nure.ua>,  # Student model
    ...            ...
    ...        ],
    ...        "<elective_group_name 2>": [
    ...            ...
    ...        ],
    ...        ...
    ...    },
    ... }
    """

    class StudentSerializer:
        """Specification how student is serialized/deserialized for RunSnapshot"""

        def __init__(self):
            self.all_students = None

        def serialize(self, student):
            return {
                "email": student.email,
                "academic_group": student.academic_group.name,
            }

        def deserialize(self, value, update_cache=False):
            if not self.all_students or update_cache:
                self.all_students = Student.objects.all().in_bulk(field_name="email")
            return self.all_students[value["email"]]

    def __init__(
        self,
        application_window: ApplicationWindow = None,
        run_snapshot: RunSnapshot = None,
    ):
        self.application_window = application_window
        self.run_snapshot = run_snapshot

        self.student_serializer = self.StudentSerializer()

    @transaction.atomic
    def run(self) -> RunSnapshot:
        if self.run_snapshot:
            return self.run_snapshot

        self.run_snapshot = RunSnapshot(strategy=Strategy.DEFAULT)

        if not self.application_window:
            raise ValueError("Application window should not be None when handler runs.")

        self.run_snapshot.application_window = self.application_window

        semesters = Semester.objects.all().prefetch_related("blocks").in_bulk()

        if len(semesters) < len(config.SEMESTERS):
            raise StrategyError(
                ErrorMessage.invalid_semesters_num.format(
                    num_of_semesters=len(config.SEMESTERS)
                )
            )

        study_years = get_study_years_by_semesters(config.SEMESTERS)
        # We subtract from stud year one to have students from previous year who
        # apply for the next year
        start_years = [
            get_start_year_by_current_study_year(study_year - 1)
            for study_year in study_years
        ]
        all_students = list(
            Student.objects.filter(academic_group__start_year__in=start_years)
        )

        all_courses_by_id = ElectiveCourse.objects.all().in_bulk()

        choices = (
            self.application_window.choices.all()
            .order_by("-update_date", "-create_date")
            .select_related("student__academic_group")
        )

        for semester_id in config.SEMESTERS:
            if semester_id not in semesters:
                raise StrategyError(
                    ErrorMessage.no_semester_config.format(semester=semester_id)
                )

            semester = semesters[semester_id]
            self.run_snapshot.need_redistribution[semester_id] = []

            # Step 1: Generate student bins for each elective course
            semester_choices = [
                choice for choice in choices if choice.semester_id == semester_id
            ]
            student_bins = self.generate_student_bins(semester_choices)

            # Step 2: Remove elective courses which did not get enough students
            short_elective_course_ids = self.check_short_elective_courses(student_bins)
            if short_elective_course_ids:
                self.log_students_from_short_elective_courses(
                    student_bins, short_elective_course_ids, semester
                )

                for elective_course_id in short_elective_course_ids:
                    del student_bins[elective_course_id]

            # Step 3: Log students who did not choose anything for this semester
            choiceless_students = self.check_choiceless_students(
                semester_choices, all_students
            )
            if choiceless_students:
                self.log_choiceless_students(choiceless_students, semester)

            # Step 4: Form groups for this semester
            self.run_snapshot.result[semester.id] = self.form_groups(
                student_bins, all_courses_by_id
            )

        self.run_snapshot.save()

        return self.run_snapshot

    def generate_student_bins(self, choices):
        """Student bins are all students applied for particular elective course"""
        student_bins = defaultdict(list)

        for choice in choices:
            for block_data in choice.value:
                for elective_course_id in block_data["elective_course_ids"]:
                    student_bins[elective_course_id].append(choice.student)

        return student_bins

    def check_short_elective_courses(self, student_bins):
        short_elective_course_ids = []
        for elective_course_id, students in student_bins.items():
            if len(students) < config.MIN_NUMBER_OF_STUDENTS_IN_ELECTIVE_GROUP:
                short_elective_course_ids.append(elective_course_id)

        return short_elective_course_ids

    def log_students_from_short_elective_courses(
        self, student_bins, elective_course_ids, semester
    ):
        for elective_course_id in elective_course_ids:
            for student in student_bins[elective_course_id]:
                self.need_redistribution[semester.id].append(
                    {
                        "student": student.id,
                        "reason": RedistributeReason.demounted_elective_course,
                        "meta": {
                            "elective_course": elective_course_id,
                        },
                    }
                )

    def check_choiceless_students(self, choices_for_semester, all_students):
        choiceful_students = []
        for choice in choices_for_semester:
            choiceful_students.append(choice.student)

        return set(all_students).difference(set(choiceful_students))

    def log_choiceless_students(self, students_without_choice, semester):
        self.need_redistribution[semester.id].extend(
            [
                {
                    "student": student.id,
                    "reason": RedistributeReason.choiceless_students,
                    "meta": {},
                }
                for student in students_without_choice
            ]
        )

    def form_groups(self, student_bins, all_courses_by_id):
        # We should sort students by academic group and full name
        for students in student_bins.values():
            students.sort(
                key=lambda s: (
                    s.academic_group.name,
                    s.last_name,
                    s.first_name,
                    s.patronymic,
                )
            )

        formed_groups = defaultdict(dict)
        for elective_course_id, students in student_bins.items():
            shortened_start_year = shorten_year(students[0].academic_group.start_year)

            group_factory = ElectiveGroupNameFactory(
                course=all_courses_by_id[elective_course_id],
                start_year=shortened_start_year,
            )

            students_num = len(students)

            for num_of_groups in range(1, config.MAX_NUMBER_OF_ELECTIVE_GROUPS + 1):
                max_students_num = (
                    num_of_groups * config.MAX_NUMBER_OF_STUDENTS_IN_ELECTIVE_GROUP
                )

                if students_num <= max_students_num:
                    group_students_num = students_num // num_of_groups
                    remainded_students_num = students_num % num_of_groups

                    group_names = group_factory.generate_many(num_of_groups)
                    for group_name, start_idx in zip(
                        group_names, range(0, students_num, group_students_num)
                    ):
                        end_idx = start_idx + group_students_num
                        if start_idx == 0:
                            # First group takes remainded students also
                            end_idx += remainded_students_num
                        else:
                            # After first group tool remainded students we should do offset to the number of remainded students
                            start_idx += remainded_students_num

                        group = students[start_idx:end_idx]
                        formed_groups[elective_course_id][group_name] = [
                            self.student_serializer.serialize(student)
                            for student in group
                        ]
                    break

        return formed_groups

    @transaction.atomic
    def save_results(self):
        if not self.run_snapshot:
            try:
                self.run_snapshot = RunSnapshot.objects.filter(
                    status=RunSnapshot.Status.ACCEPTED
                ).latest("update_date")
            except RunSnapshot.DoesNotExist:
                raise StrategyError(
                    _("No run snapshot was found for this application window.")
                )

        if self.run_snapshot.status != RunSnapshot.Status.ACCEPTED:
            raise StrategyError(
                _(
                    "Status of run snapshot should be ACCEPTED before making elective groups permanent."
                )
            )

        validate_schema(
            self.run_snapshot.need_redistribution,
            DefaultStrategySchemas.EMPTY_NEED_REDISTRIBUTION,
            exc_cls=StrategyError,
            exc_msg=_(
                "All students should be redistributed before making elective groups permanent."
            ),
        )

        choices_by_student = {}
        for choice in self.run_snapshot.application_window.choices.all():
            choices_by_student[choice.student_id] = choice

        for _semester_id_key, elecitve_courses in self.run_snapshot.result.items():
            for elective_course_id_key, groups in elecitve_courses.items():
                elective_course_id = int(elective_course_id_key)

                for group_name, serialized_students in groups.items():
                    elective_group, _created = ElectiveGroup.objects.get_or_create(
                        name=group_name,
                        elective_course_id=elective_course_id,
                        start_year=get_start_year_by_group_name(group_name),
                    )

                    for serialized_student in serialized_students:
                        student = self.student_serializer.deserialize(
                            serialized_student
                        )
                        ElectiveGroupStudentAssociation.objects.get_or_create(
                            elective_group=elective_group,
                            student=student,
                            choice=choices_by_student[student.id],
                        )

    # def add_students_without_choice(self, student_bins, students_without_choice, semester):
    #     meta_info = {}
    #     for block in semester.blocks.all().prefetch_related("elective_courses"):
    #         available_seats_list = []
    #         unrestricted_seats_list = []

    #         for elective_course in block.elective_courses.all():
    #             occupied_seats = len(student_bins[elective_course.id])
    #             all_seats = elective_course.capacity or block.capacity  # If elective course has capacity, it overrides the block one

    #             if all_seats is None:
    #                 # Neither elective course nor block restrict number of seats
    #                 unrestricted_seats_list.append(elective_course)
    #                 meta_info[elective_course] = {
    #                     "occupied_seats": occupied_seats
    #                 }

    #             elif occupied_seats < all_seats:
    #                 available_seats_list.append(elective_course)
    #                 meta_info[elective_course] = {
    #                     "available_percent": occupied_seats / all_seats
    #                 }

    #         ordered_unrestricted_seats_list = sorted(
    #             unrestricted_seats_list, key=lambda u: meta_info[u]["occupied_seats"]
    #         )
    #         ordered_available_seats_list = sorted(
    #             available_seats_list, key=lambda u: meta_info[u]["available_percent"], reverse=True
    #         )

    # def check_capacity_violation(self, student_bins, elective_units):
    #     """Check if any unit exceeds maximum capacity of students"""

    #     violated_units = []
    #     meta_info = {}
    #     for elective_unit in elective_units:
    #         current_capacity = len(student_bins[elective_unit.id])
    #         max_capacity = elective_unit.capacity or CAPACITY_NOT_RESTRICTED

    #         if current_capacity > max_capacity:
    #             violated_units.append(elective_unit)
    #             meta_info[elective_unit] = {
    #                 "students_overflow": current_capacity - max_capacity,
    #             }

    #     return violated_units, meta_info

    # def solve_violation(
    #     self, student_bins, violated_units, violated_unit_meta, elective_units
    # ):
    #     student_bins = self.solve_capacity_violation(
    #         student_bins, violated_units, violated_unit_meta, elective_units
    #     )

    #     return student_bins

    # def solve_capacity_violation(
    #     self, student_bins, violated_units, violated_unit_meta, elective_units
    # ):
    #     meta_info = {**violated_unit_meta}

    #     available_units = []
    #     for elective_unit in elective_units:
    #         if elective_unit in violated_units:
    #             continue

    #         current_capacity = len(student_bins[elective_unit.id])
    #         max_capacity = elective_unit.capacity

    #         available_places_num = max_capacity - current_capacity

    #         available_units.append(elective_unit)
    #         meta_info[elective_unit] = {"available_places": available_places_num}

    #     ordered_violated_units = sorted(
    #         violated_units,
    #         key=lambda u: meta_info[u]["students_overflow"],
    #         reverse=True,
    #     )
    #     ordered_available_units = sorted(
    #         available_units,
    #         key=lambda u: meta_info[u]["available_places"],
    #         reverse=True,
    #     )

    #     for available_unit in ordered_available_units:
    #         for violated_unit in ordered_violated_units:

    #             students_overflow_num = meta_info[violated_unit]["students_overflow"]
    #             available_places_num = meta_info[available_unit]["available_places"]

    #             if students_overflow_num < available_places_num:
    #                 migrating_students = violated_unit.pop(students_overflow_num)
    #                 student_bins[available_unit].append(migrating_students)

    #                 meta_info[available_unit]["available_places"] =
