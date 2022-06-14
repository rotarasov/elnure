import enum

from faker import Faker
from factory.fuzzy import BaseFuzzyAttribute

fake = Faker(locale="ru_RU")


class SEX(enum.Enum):
    MALE = "m"
    FEMALE = "f"


class SexMixin:
    def __init__(self, sex=SEX.MALE, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._sex = sex


class FuzzyFullName(SexMixin, BaseFuzzyAttribute):
    FULL_NAME_GENERATOR_BY_SEX = {
        SEX.MALE: lambda f: f"{f.last_name_male()} {f.middle_name_male} {f.first_name_male}",
        SEX.FEMALE: lambda f: f"{f.last_name_female()} {f.middle_name_female} {f.first_name_female}",
    }

    def fuzz(self):
        return self.FULL_NAME_GENERATOR_BY_SEX[self._sex]


class FuzzyFirstName(SexMixin, BaseFuzzyAttribute):
    FIRST_NAME_GENERATOR_BY_SEX = {
        SEX.MALE: lambda f: f.first_name_male,
        SEX.FEMALE: lambda f: f.first_name_female,
    }

    def fuzz(self):
        return self.FIRST_NAME_GENERATOR_BY_SEX[self._sex]


class FuzzyLastName(SexMixin, BaseFuzzyAttribute):
    LAST_NAME_GENERATOR_BY_SEX = {
        SEX.MALE: lambda f: f.last_name_male,
        SEX.FEMALE: lambda f: f.last_name_female,
    }

    def fuzz(self):
        return self.LAST_NAME_GENERATOR_BY_SEX[self._sex]


class FuzzyPatronymicName(SexMixin, BaseFuzzyAttribute):
    PATRONYMIC_GENERATOR_BY_SEX = {
        SEX.MALE: lambda f: f.middle_name_male,
        SEX.FEMALE: lambda f: f.middle_name_female,
    }

    def fuzz(self):
        return self.PATRONYMIC_GENERATOR_BY_SEX[self._sex]
