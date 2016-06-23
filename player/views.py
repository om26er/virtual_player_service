from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework import permissions, status
from rest_framework.response import Response

from player.serializers import UserSerializer


class UserRegistrationView(CreateAPIView):
    serializer_class = UserSerializer


class RetrieveUpdateDestroyProfile(RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserSerializer
    http_method_names = ['patch', 'get', 'delete']

    def get_queryset(self):
        return self.request.user

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        # If the request included an email change request,
        # reply with 403.
        email = request.data.get('email')
        if email:
            return Response(
                {'email': 'Cannot be changed.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
