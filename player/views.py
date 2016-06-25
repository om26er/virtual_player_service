from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response

from player.serializers import UserSerializer


class UserRegistrationView(CreateAPIView):
    serializer_class = UserSerializer


class RetrieveUpdateDestroyProfile(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserSerializer
    http_method_names = ['put', 'get', 'delete']

    def get(self, *args, **kwargs):
        serializer = UserSerializer(instance=self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, *args, **kwargs):
        self.request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, *args, **kwargs):
        email = self.request.data.get('email')
        if email:
            return Response(
                {'email': 'Not allowed to change email.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = UserSerializer(
            instance=self.request.user,
            data=self.request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Make sure to hash the password, in case it was changed.
        password = self.request.data.get('password')
        if password:
            self.request.user.set_password(password)
            self.request.user.save()
        return Response(status=status.HTTP_200_OK)
