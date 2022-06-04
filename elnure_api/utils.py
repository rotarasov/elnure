from datetime import datetime
from functools import lru_cache
from math import ceil


@lru_cache
def get_current_month_year() -> tuple[int, int]:
    now = datetime.now()
    return now.month, now.year


# Study year -- Start year


def get_current_study_year_by_start_year(start_year: int) -> int:
    """Returning current study year of the group for particular start year"""
    current_month, current_year = get_current_month_year()
    next_year = (
        current_month // 9
    )  # July and August are also considered as previous year
    return current_year - start_year + next_year


def get_start_year_by_current_study_year(study_year: int) -> int:
    """Retrun study year by academic group start year"""
    current_month, current_year = get_current_month_year()
    next_year = (
        current_month // 9
    )  # July and August are also considered as previous year
    return current_year - study_year + next_year


# Semester -- Study year


def get_study_years_by_semesters(semester_ids: list[int]) -> list[int]:
    """Returning list of study years for the semesters"""
    return list(set([ceil(s / 2) for s in semester_ids]))


def get_study_year_by_semester(semester_id: int) -> int:
    return get_study_years_by_semesters([semester_id])[0]


def get_semesters_by_study_year(study_year: int) -> list[int]:
    """Returning semester numbers for study year"""
    return [study_year * 2 - 1, study_year * 2]


# Elective Group


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
