from django.db import models

from elnure_common.models import CommonModel


class Semester(CommonModel):
    id = models.PositiveIntegerField(
        primary_key=True, help_text="Id should be equal to the number of the semester."
    )
    total_credits = models.PositiveIntegerField(
        help_text="How many credits in total should be covered by electives"
    )
    study_year = models.PositiveIntegerField()

    class Meta:
        db_table = "semesters"

    def __str__(self) -> str:
        return f"Semester {self.id}"


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
