from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):

    def _raise_if_email_or_password_missing(self, email, password):
        if not email and not password:
            raise ValueError('Email and Password are mandatory.')

        if not email:
            raise ValueError('Email is mandatory.')

        if not password:
            raise ValueError('Password is mandatory.')

    def create_user(self, email, password=None, **extra_fields):
        self._raise_if_email_or_password_missing(email, password)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        return self.create_user(email, password, is_admin=True, **extra_fields)
