from ..models import User, ActivationKey, PasswordResetKey

from ..helpers import generate_random_key


class UserHelpers:
    def __init__(self, **kwargs):
        self.user = User.objects.get(**kwargs)

    def is_active(self):
        return self.user.is_active

    def is_admin(self):
        return self.user.is_admin

    def can_be_activated(self):
        return not self.is_admin() and not self.is_active()

    def set_password_reset_key(self, key):
        try:
            key_object = PasswordResetKey.objects.get(user=self.user)
        except PasswordResetKey.DoesNotExist:
            key_object = PasswordResetKey.objects.create(user=self.user)

        key_object.key = int(key)
        key_object.save()

    def get_password_reset_key(self):
        return int(PasswordResetKey.objects.get(user=self.user).key)

    def _reset_password_reset_key(self):
        password_object = PasswordResetKey.objects.get(user=self.user)
        password_object.key = -1
        password_object.save()

    def is_password_reset_key_valid(self, key):
        return self.get_password_reset_key() == int(key)

    def change_password(self, new_password):
        self.user.set_password(new_password)
        self.user.save()
        self._reset_password_reset_key()

    def is_account_activation_key_valid(self, activation_key):
        if int(activation_key) == -1:
            return False
        key = ActivationKey.objects.get(user=self.user)
        return int(key.key) == int(activation_key)

    def activate(self):
        key = ActivationKey.objects.get(user=self.user)
        key.key = -1
        self.user.is_active = True
        self.user.save()
        key.save()
