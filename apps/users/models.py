from django.db import models

from core.models import BaseModel

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from apps.users.managers import UserManager


class UserModel(AbstractBaseUser, PermissionsMixin, BaseModel):
    class Meta:
        db_table = 'staff_and_admin'
        ordering = ['-id']

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    activation_token = models.CharField(max_length=64, blank=True, null=True)
    activation_token_expires_at = models.DateTimeField(null=True,blank=True)
    objects = UserManager()
