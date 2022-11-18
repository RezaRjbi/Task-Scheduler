from rest_framework.views import APIView, status
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError

from .models import User
from . import serializers as cs
from .permissions.permissions import IsAdminOrNewUser, IsSuperuser
from .permissions.permissions import CustomPermissions as Cp

from utils.general import response
from utils.db import update_instance


class ListCreateUserView(APIView):
    permission_classes = [IsAdminOrNewUser]

    def get(self, request):
        users = User.objects.all()
        return response(
            instance=users, serializer=cs.UserSerializer, many=True, total=users.count(), status_code=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = cs.RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            try:

                user = User.objects.create_user(**serializer.data)
            except IntegrityError as e:
                return response(
                    status_code=status.HTTP_400_BAD_REQUEST, errors=str(e), detail="username already exists"
                )
            return response(instance=user, status_code=status.HTTP_201_CREATED, serializer=cs.UserSerializer)
        return response(errors=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)


class RetrieveUpdateDestroyUserView(APIView):

    @Cp.is_admin_or_owner
    def get(self, request, pk: int):
        user = get_object_or_404(User, pk=pk)
        return response(instance=user, serializer=cs.UserSerializer, status_code=status.HTTP_200_OK)

    @Cp.is_owner
    def put(self, request, pk: int):
        user = get_object_or_404(User, pk=pk)
        serializer = cs.UpdateUserSerializer(data=request.data)
        if serializer.is_valid():
            update_instance(user, serializer.data)
            return response(status_code=status.HTTP_200_OK, instance=user, serializer=cs.UserSerializer)

        return response(errors=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)

    @Cp.is_admin
    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return response(status_code=status.HTTP_204_NO_CONTENT, detail="user deleted")


class LoginView(APIView):

    def post(self, request, format=None):

        serializer = cs.LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return response(errors=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)
        data = serializer.data
        try:
            User.objects.get(username=data.get("username"))
        except User.DoesNotExist as e:
            return response(detail="user not found", errors=str(e), status_code=status.HTTP_404_NOT_FOUND)
        user = authenticate(username=data.get("username"), password=data.get("password"))
        if not user:
            return response(
                detail="provided username and password dont match",
                errors="wrong_credentials", status_code=status.HTTP_401_UNAUTHORIZED
            )
        login(request, user)
        token = Token.objects.get_or_create(user=user)
        return response(
            detail=f"{user.username} logged in successfully",
            status_code=status.HTTP_200_OK, token=token[0].key
        )


class LogoutView(APIView):

    def post(self, request, format=None):
        logout(request)
        request.user.auth_token.delete()
        return response(detail="Successfully logged out", status_code=status.HTTP_200_OK)


class ChangeRoleView(APIView):
    """
    a superuser can promote a normal user to a staff member or turn a staff member to a normal user
    """
    permission_classes = [IsSuperuser]

    def post(self, request, pk):
        serializer = cs.ChangeRoleSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(User, pk=pk)
            update_instance(user, serializer.data)
            return response(status_code=status.HTTP_200_OK)
        return response(status_code=status.HTTP_400_BAD_REQUEST, errors=serializer.errors)


class ChangeActiveStatusView(APIView):
    """
    turn a user active status to de-active and vice-versa
    """

    @Cp.is_admin
    def post(self, request, pk):
        serializer = cs.ChangeActiveStatusSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(User, pk=pk)
            update_instance(user, serializer.data)
            return response(status_code=status.HTTP_200_OK)
        return response(status_code=status.HTTP_400_BAD_REQUEST, errors=serializer.errors)


class DeleteAccountView(APIView):
    """
    only account owner them-self can use this views. mods can CahngeActiveStatusView to ban/unban users
    """

    @Cp.is_owner
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        update_instance(user, {"is_active": False})
        return response(status_code=status.HTTP_200_OK, detail="Account successfully deleted")


class MeView(APIView):

    @Cp.has_permission(['is_authenticated'])
    def get(self, request):
        return response(status_code=status.HTTP_200_OK, instance=request.user, serializer=cs.UserSerializer)

# todo: use new permission decorator on views
