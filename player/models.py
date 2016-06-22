from django.db import models

from simple_login.models import BaseUser


class User(BaseUser):
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    school = models.CharField(max_length=255, blank=True)
