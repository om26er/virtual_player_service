from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .models import User
from .serializers import UserSerializer
from .helpers import generate_random_key, send_password_reset_email
from .helpers.response_helpers import ResponseConstructor
from .helpers.user_helpers import UserHelpers


class UserRegistrationView(CreateAPIView):
    serializer_class = UserSerializer


class UserActivationView(APIView):
    def _validate_parameters(self, email, key):
        response_constructor = ResponseConstructor()
        response_constructor.validate_field('email', email)
        response_constructor.validate_field('key', key)
        return response_constructor.get_response()

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        key = request.data.get('key')
        message = self._validate_parameters(email, key)
        if message:
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_account = UserHelpers(email=email)
            if user_account.can_be_activated():
                if user_account.is_account_activation_key_valid(key):
                    user_account.activate()
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_304_NOT_MODIFIED)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserDetailsView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordResetView(APIView):
    def _validate_parameters(self, email):
        response_constructor = ResponseConstructor()
        response_constructor.validate_field('email', email)
        return response_constructor.get_response()

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        message = self._validate_parameters(email)
        if message:
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_account = UserHelpers(email=email)
            if user_account.is_active():
                if user_account.is_admin():
                    return Response(status=status.HTTP_403_FORBIDDEN)
                user_account.set_password_reset_key(generate_random_key())
                send_password_reset_email(
                    email,
                    user_account.get_password_reset_key()
                )
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(
                    data={'email': ['Account not active.']},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except User.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )


class ChangePasswordView(APIView):
    def _validate_parameters(self, email, reset_key, new_password):
        response_constructor = ResponseConstructor()
        response_constructor.validate_field('email', email)
        response_constructor.validate_field('reset_key', reset_key)
        response_constructor.validate_field('new_password', new_password)
        return response_constructor.get_response()

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        reset_key = request.data.get('reset_key')
        new_password = request.data.get('new_password')
        message = self._validate_parameters(email, reset_key, new_password)
        if message:
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_account = UserHelpers(email=email)
            if user_account.is_admin():
                return Response(status=status.HTTP_403_FORBIDDEN)
            if user_account.is_password_reset_key_valid(reset_key):
                user_account.change_password(new_password)
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(
                    data={'reset_key': ['Invalid']},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except User.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )