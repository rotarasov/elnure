from random import choice
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

from elnure_common.fields import ElnureEnumField
from elnure_common.models import CommonModel, StudentGroupMixin, SemesterMixin


class Instructor(CommonModel):
    full_name = models.CharField(max_length=150)

    class Meta:
        db_table = "instructors"

    def __str__(self) -> str:
        return self.full_name


class Block(CommonModel):
    name = models.CharField(max_length=150)
    credits = models.IntegerField(null=True, validators=[MinValueValidator(1)])

    class Meta:
        db_table = "blocks"

    def __str__(self) -> str:
        return f"{self.name}({self.courses.count()})"


class ElectiveCourse(SemesterMixin, CommonModel):
    class PerformanceAssessment(models.TextChoices):
        SESSION_EXAMINATION = "SESSION_EXAMINATION"
        GRADED_SEMESTER = "GRADED_SEMESTER"

    name = models.CharField(max_length=50)
    shortcut = models.CharField(max_length=10)
    syllabus = models.CharField(max_length=300)
    capacity = models.IntegerField(null=True, validators=[MinValueValidator(1)])
    credits = models.IntegerField(validators=[MinValueValidator(1)])
    performance_assessment = ElnureEnumField(
        PerformanceAssessment, default=PerformanceAssessment.GRADED_SEMESTER
    )
    block = models.ForeignKey(
        Block, on_delete=models.SET_NULL, null=True, blank=True, related_name="courses"
    )
    instructors = models.ManyToManyField(
        Instructor,
        related_name="assigned_courses",
        through="InstructorAssignment",
    )

    class Meta:
        db_table = "elective_courses"

    def __str__(self) -> str:
        return self.shortcut


class InstructorAssignment(CommonModel):
    class Position(models.TextChoices):
        LECTURER = "LECTURER"
        ASSISTANT = "ASSISTANT"

    to_elective_course = models.ForeignKey(ElectiveCourse, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    position = ElnureEnumField(Position)

    class Meta:
        db_table = "instructor_assignment"

    def __str__(self) -> str:
        return f"{self.elective_course.shortcut} -- {self.instructor.full_name} as {self.position}"


class ElectiveGroup(StudentGroupMixin, CommonModel):
    elective_course = models.ForeignKey(
        ElectiveCourse, on_delete=models.CASCADE, related_name="groups"
    )

    class Meta:
        db_table = "elective_groups"

    def __str__(self) -> str:
        return self.name


class ApplicationWindow(CommonModel):
    """
    Entity to configure flow of student applications for elective courses
    """

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        db_table = "application_windows"

    def __str__(self) -> str:
        return f"#{self.id}: {self.start_date} - {self.end_date}"


# TODO: Add strategy field
class Choice(CommonModel):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="elective_course_choices",
    )
    study_year = models.IntegerField(
        help_text="Study year of elective courses which student applies for",
        validators=[MinValueValidator(2), MaxValueValidator(4)],
    )
    value = models.JSONField(
        help_text="Value to be processed in one of the descendants of BaseChoiceHandler"
    )
    elective_groups = models.ManyToManyField(
        ElectiveGroup,
        related_name="students_choices",
        help_text="Elective groups attached to students after groups formation",
    )
    application_window = models.ForeignKey(
        ApplicationWindow,
        on_delete=models.SET_NULL,
        related_name="choices",
        null=True,
    )

    class Meta:
        db_table = "choices"
        unique_together = ["student", "application_window"]

    def __str__(self) -> str:
        return f"{self.student.get_full_name()} -- {self.study_year} study year"
