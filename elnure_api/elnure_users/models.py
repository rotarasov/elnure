from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

from elnure_common.models import CommonModel
from elnure_users.managers import UserManager


class User(CommonModel, AbstractUser):
    username = None
    date_joined = None

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    patronymic = models.CharField(max_length=150, blank=True, null=True)
    academic_group = models.ForeignKey(
        "AcademicGroup", on_delete=models.RESTRICT, related_name="students"
    )
    roles = models.ManyToManyField("Role", related_name="users")

    @property
    def is_active(self):
        return bool(self.active > 0)

    @property
    def is_admin(self):
        return bool(self.roles.count(name="Adminsistrator"))

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self) -> str:
        return self.email

    class Meta:
        db_table = "users"


class Role(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=150)

    class Meta:
        db_table = "roles"


class AcademicGroup(CommonModel):
    name = models.CharField(max_length=30)

    def get_start_year(self):
        """When academic group was formed.
        First part states for department
        Second part states for start year
        Third part states for group number
        ex. ПЗПІ-18-5 => 2018
        """
        row_year = self.name.split("-")[1]
        return datetime.strptime("%y", row_year)

    class Meta:
        db_table = "academic_groups"
