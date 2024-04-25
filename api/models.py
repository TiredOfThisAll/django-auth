from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=200, unique=True)
    invite_code = models.CharField(max_length=12, unique=True)
    invited_by = models.CharField(max_length=12, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    last_login = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()

    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
        'phone_number',
        'password',
        'invite_code'
    ]

    def __str__(self):
        return self.username
