from django.db import models

from core.models import BaseModel

from django.core import validators as V

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from apps.users.managers import UserManager


class UserModel(AbstractBaseUser, PermissionsMixin, BaseModel):
    class Meta:
        db_table = 'staff_and_admin'
        ordering = ['-id']

    email = models.EmailField(unique=True, validators=[V.validate_email], blank=False)
    name = models.CharField(max_length=20, validators=(V.MinLengthValidator(1),), blank=False)
    surname = models.CharField(max_length=20, validators=(V.MinLengthValidator(1),), blank=False)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    objects = UserManager()
