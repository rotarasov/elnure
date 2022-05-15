import enum

from faker import Faker
from factory.fuzzy import BaseFuzzyAttribute

fake = Faker()


class SEX(enum.Enum):
    MALE = "m"
    FEMALE = "f"


class FuzzyFullName(BaseFuzzyAttribute):
    FULL_NAME_GENERATOR_BY_SEX = {
        SEX.MALE: lambda f: f"{f.last_name_male()} {f.middle_name_male} {f.first_name_male}",
        SEX.FEMALE: lambda f: f"{f.last_name_female()} {f.middle_name_female} {f.first_name_female}",
    }

    def __init__(self, sex: SEX = SEX.MALE):
        super().__init__()
        self._sex = sex

    def fuzz(self):
        return self.FULL_NAME_GENERATOR_BY_SEX[self._sex]
