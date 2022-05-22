from django.contrib.auth.models import Group, BaseUserManager
from django.contrib.auth.hashers import make_password

from elnure_common.managers import ActiveManager


class UserManager(BaseUserManager):
    def _create_user(self, email, first_name, last_name, password=None, **extra_fields):
        """
        Create and save a user with the given email, password, first_name and last_name, etc.
        """
        if not email:
            raise ValueError("The given email must be set")
        if not first_name:
            raise ValueError("The given first_name must be set")
        if not last_name:
            raise ValueError("The given last_name must be set")

        if not password:
            password = self.make_random_password(length=16)

        email = self.normalize_email(email)
        user = self.model(
            email=email, first_name=first_name, last_name=last_name, **extra_fields
        )
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, first_name, last_name, **extra_fields):
        return self._create_user(email, first_name, last_name, **extra_fields)

    def create_superuser(self, email, first_name, last_name, **extra_fields):
        superuser = self._create_user(email, first_name, last_name, **extra_fields)
        try:
            superuser.groups.add(Group.objects.get(name="Administrator"))
        except Group.DoesNotExist:
            raise Group.DoesNotExist("No Administrator group exists")
        return superuser


class ActiveUserManager(ActiveManager, UserManager):
    pass
