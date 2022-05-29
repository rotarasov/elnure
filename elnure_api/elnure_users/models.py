from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from elnure_common.models import (
    CommonModel,
    ActiveMixin,
    StudentGroupMixin,
)
from elnure_users.managers import UserManager, ActiveUserManager, StudentManager


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
    is_admin = models.BooleanField(
        default=False, help_text="Whether user should be admin"
    )

    @property
    def is_active(self):
        return bool(self.active > 0)

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


class Student(User):
    objects = StudentManager()

    class Meta:
        proxy = True


class AcademicGroup(StudentGroupMixin, CommonModel):
    class Meta:
        db_table = "academic_groups"

    def __str__(self) -> str:
        return self.name
