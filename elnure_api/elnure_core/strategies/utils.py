from datetime import datetime

from elnure_core.models import ElectiveCourse


class ElectiveGroupNameFactory:
    """
    Generating
    """

    DEFAULT_PREFIX = "ПЗПІ"
    DEFAULT_TEMPLATE = "{prefix}[{shorcut}]-{start_year}-{index}"

    def __init__(
        self,
        course: ElectiveCourse,
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
