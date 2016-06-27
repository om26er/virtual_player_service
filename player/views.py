from rest_framework.generics import CreateAPIView
from simple_login.views import (
    RetrieveUpdateDestroyProfileView,
    AccountActivationAPIView,
    LoginAPIView,
)

from player.serializers import UserSerializer


class UserRegistrationView(CreateAPIView):
    serializer_class = UserSerializer


class RetrieveUpdateDestroyProfile(RetrieveUpdateDestroyProfileView):
    serializer_class = UserSerializer


class ActivateAccount(AccountActivationAPIView):
    serializer_class = UserSerializer


class Login(LoginAPIView):
    serializer_class = UserSerializer
