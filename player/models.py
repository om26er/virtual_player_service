from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

from .managers import CustomUserManager
from .helpers import generate_random_key, send_account_activation_email
from virtual_player_service.settings import AUTH_USER_MODEL


@receiver(post_save, sender=AUTH_USER_MODEL)
def finalize_account_creation(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

        if not instance.is_admin:
            activation_key = ActivationKey.objects.create(user=instance)
            PasswordResetKey.objects.create(user=instance)
            send_account_activation_email(instance.email, activation_key.key)
            instance.set_password(instance.password)
            instance.is_active = False
            instance.save()


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, blank=False, unique=True)
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    school = models.CharField(max_length=255, blank=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True, blank=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class ActivationKey(models.Model):
    user = models.OneToOneField(
        AUTH_USER_MODEL,
        related_name='activation_key',
        on_delete=models.CASCADE,
        verbose_name='Account activation keys'
    )
    key = models.IntegerField(default=-1)

    def save(self, *args, **kwargs):
        self.key = generate_random_key()
        return super().save(*args, **kwargs)


class PasswordResetKey(models.Model):
    user = models.OneToOneField(
        AUTH_USER_MODEL,
        related_name='password_reset_key',
        on_delete=models.CASCADE,
        verbose_name='Password reset keys'
    )
    key = models.IntegerField(default=-1)

    def save(self, *args, **kwargs):
        self.key = generate_random_key()
        return super().save(*args, **kwargs)
