from email.policy import default

from django.db import models

from core.models import BaseModel

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from apps.users.managers import UserManager


class UserModel(AbstractBaseUser, PermissionsMixin, BaseModel):
    class Meta:
        db_table = 'staff_and_admin'
        ordering = ['id']

    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    objects = UserManager()
