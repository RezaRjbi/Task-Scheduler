from rest_framework.views import APIView, status
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth import authenticate, login, logout

from pydantic import ValidationError

from .models import User
from .serializers import UserSerializer, LoginSerializer

from .permissions import IsUnAuthenticated


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer


class LoginView(APIView):
    permission_classes = [IsUnAuthenticated]

    def post(self, request, format=None):
        try:
            data = LoginSerializer(**request.data)
        except ValidationError as e:
            return Response(dict(errors=e.errors()))
        try:
            User.objects.get(username=data.username)
        except User.DoesNotExist:
            return Response(dict(errors="user not found"), status=status.HTTP_404_NOT_FOUND)
        user = authenticate(username=data.username, password=data.password)
        if not user:
            return Response(dict(errors="Wrong credentials"))
        login(request, user)
        return Response(dict(success=f"{user.username} successfully logged in"), status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        logout(request)
        return Response(dict(success="Successfully logged out"))
