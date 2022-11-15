from rest_framework.views import APIView, status
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from .models import User
from .serializers import UserSerializer, LoginSerializer, UpdateUserSerializer

from .permissions import IsAdminOrNewUser

from utils.general import response
from utils.db import update_instance


class ListCreateUserView(APIView):
    # permission_classes = [IsAdminOrNewUser]

    def get(self, request):
        users = User.objects.all()
        return response(
            instance=users, serializer=UserSerializer, many=True, total=users.count(), status_code=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return response(instance=user, status_code=status.HTTP_201_CREATED, serializer=UserSerializer)
        return response(errors=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)


class RetrieveUpdateDestroyUserView(APIView):
    def get(self, request, pk: int):
        user = get_object_or_404(User, pk=pk)
        return response(instance=user, serializer=UserSerializer, status_code=status.HTTP_200_OK)

    def put(self, request, pk: int):
        user = get_object_or_404(User, pk=pk)
        serializer = UpdateUserSerializer(data=request.data)
        if serializer.is_valid():
            update_instance(user, serializer.data)
            return response(status_code=status.HTTP_200_OK, instance=user, serializer=UserSerializer)

        return response(errors=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return response(status_code=status.HTTP_204_NO_CONTENT, detail="user deleted")


class LoginView(APIView):

    def post(self, request, format=None):

        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return response(errors=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)
        data = serializer.data
        try:
            User.objects.get(username=data["username"])
        except User.DoesNotExist as e:
            return response(detail="user not found", errors=str(e), status_code=status.HTTP_404_NOT_FOUND)
        user = authenticate(username=data["username"], password=data["password"])
        if not user:
            return response(
                detail="provided username and password dont match",
                errors="wrong_credentials", status_code=status.HTTP_401_UNAUTHORIZED
            )

        token = Token.objects.get_or_create(user=user)
        return response(
            detail=f"{user.username} logged in successfully",
            status_code=status.HTTP_200_OK, token=token[0].key
        )


class LogoutView(APIView):

    def post(self, request, format=None):
        request.user.auth_token.delete()
        return response(detail="Successfully logged out", status_code=status.HTTP_200_OK)


class ChangeRoleView(APIView):
    """
    a superuser can promote or a normal user to a staff member or turn a staff member to a normal one
    """

    def post(self):
        # todo
        ...


class ChangeUserActivateStatusView(APIView):
    """
    turn a user active status to de-active and vice-versa. only staff members can perform this action
    """
    def post(self):
        # todo
        ...
