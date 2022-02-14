from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

from elnure_common.models import CommonModel, ActiveMixin
from elnure_users.managers import UserManager


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

    objects = UserManager()

    def get_full_name(self):
        full_name = f"{self.last_name} {self.first_name}"
        if self.patronymic:
            full_name += f" {self.patronymic}"
        return full_name

    def __str__(self) -> str:
        return self.email

    class Meta:
        db_table = "users"


class AcademicGroup(CommonModel):
    name = models.CharField(max_length=30)

    def get_start_year(self):
        """When academic group was formed.
        First part states for department
        Second part states for start year
        Third part states for group number
        ex. SE-18-5 => 2018
        """
        row_year = self.name.split("-")[1]
        return datetime.strptime("%y", row_year)

    class Meta:
        db_table = "academic_groups"
