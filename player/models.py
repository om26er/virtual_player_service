from django.db import models

from simple_login.models import BaseUser


class User(BaseUser):
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    school = models.CharField(max_length=255, blank=True)

# Ensure the user account is active by default, to skip
# account activation.
User._meta.get_field('is_active').default = True
