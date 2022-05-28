from datetime import datetime
from functools import lru_cache
from math import ceil


@lru_cache
def get_current_month_year() -> tuple[int, int]:
    now = datetime.now()
    return now.month, now.year


def get_current_study_year(
    current_month: int, current_year: int, start_year: int
) -> int:
    """
    Taking current date and group's start year to calculate current study year
    NOTE: It is important to pay attention to the season of the year
    e.g. Group: SE-19-5
    Season: spring 2022 => StudyYear.THIRD
    Season: autumn 2022 => StudyYear.FOURTH
    """
    next_year = (
        current_month // 9
    )  # July and August are also considered as previous year
    return current_year - start_year + next_year


def get_all_study_years(starting_semester: int, ending_semester: int):
    """Returning list of study years for the semesters"""
    return [
        ceil(s / 2)
        for s in range(starting_semester, ending_semester + ending_semester % 2 + 1, 2)
    ]


class ElectiveGroupNameFactory:
    """
    Generating the names for elective groups
    Default name is 'ПЗПІ[АОФМ]-18-5'
    """

    DEFAULT_PREFIX = "ПЗПІ"
    DEFAULT_TEMPLATE = "{prefix}[{shorcut}]-{start_year}-{index}"

    def __init__(
        self,
        course,
        start_year: int,
        prefix: str = None,
        template: str = None,
    ):
        self.course = course
        self.start_year = start_year
        self.prefix = prefix or self.DEFAULT_PREFIX
        self.template = template or self.DEFAULT_TEMPLATE

    def generate_many(self, group_num: int) -> list[str]:
        return [
            self.template.format(
                prefix=self.prefix,
                shortcut=self.course.shortcut,
                start_year=self.start_year,
                index=index,
            )
            for index in range(1, group_num + 1)
        ]
