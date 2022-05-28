from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from elnure_common.models import (
    CommonModel,
    ActiveMixin,
    StudentGroupMixin,
)
from elnure_users.managers import UserManager, ActiveUserManager


def validate_ratings(value):
    if not isinstance(value, list):
        raise ValidationError("Ratings should be a list of int values.")
    if len(value) != 5:
        raise ValidationError(
            "5 ratings should be presented in the array(Use -1 to mark absense of rating for particular semester)."
        )
    if any(not isinstance(rating, float) for rating in value):
        raise ValidationError("All values should be float.")
    return value


class User(ActiveMixin, CommonModel, AbstractUser):
    username = None
    date_joined = None

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    patronymic = models.CharField(max_length=150, blank=True, null=True)
    academic_group = models.ForeignKey(
        "AcademicGroup", on_delete=models.RESTRICT, related_name="students", null=True
    )
    elective_groups = models.ManyToManyField(
        "elnure_core.ElectiveGroup",
        related_name="students",
        through="elnure_core.ElectiveGroupStudentAssociation",
        help_text="Elective groups attached to the student after groups formation",
    )

    @property
    def is_active(self):
        return bool(self.active > 0)

    @property
    def is_admin(self):
        return self.groups.exists(name="Adminsistrator")

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    unfiltered = UserManager()
    objects = ActiveUserManager()

    def get_full_name(self):
        full_name = f"{self.last_name} {self.first_name}"
        if self.patronymic:
            full_name += f" {self.patronymic}"
        return full_name

    def __str__(self) -> str:
        return self.email

    class Meta:
        db_table = "users"
        _default_manager = "objects"

    def __str__(self) -> str:
        return self.email


class AcademicGroup(StudentGroupMixin, CommonModel):
    class Meta:
        db_table = "academic_groups"

    def __str__(self) -> str:
        return self.name
