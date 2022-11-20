from rest_framework.views import APIView, status
from rest_framework.authtoken.models import Token

from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError

from .models import User
from . import serializers as cs
from .permissions.permissions import has_permission
from .permissions import filters

from utils.general import response, unauthorized
from utils.db import update_instance


class ListCreateUserView(APIView):

    @has_permission([filters.IS_STAFF])
    def get(self, request):
        users = User.objects.all()
        if request.query_params.get(filters.IS_ACTIVE):
            users = users.filter(is_active=True)
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

    @has_permission([filters.IS_STAFF, filters.IS_OWNER], "pk", "User")
    def get(self, request, pk: int):
        user = get_object_or_404(User, pk=pk)
        return response(instance=user, serializer=cs.UserSerializer, status_code=status.HTTP_200_OK)

    @has_permission([filters.IS_OWNER], "pk", "User")
    def put(self, request, pk: int):
        user = get_object_or_404(User, pk=pk)
        serializer = cs.UpdateUserSerializer(data=request.data)
        if serializer.is_valid():
            update_instance(user, serializer.data)
            return response(status_code=status.HTTP_200_OK, instance=user, serializer=cs.UserSerializer)

        return response(errors=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)

    @has_permission([filters.IS_STAFF])
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

        user = get_object_or_404(User, username=data.get("username"))
        if not user.is_active:

            return unauthorized()

        if not user.check_password(data.get("password")):
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
    @has_permission([filters.IS_SUPERUSER])
    def put(self, request, pk):
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

    @has_permission([filters.IS_STAFF])
    def put(self, request, pk):
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

    @has_permission([filters.IS_OWNER], kw="pk", model_filed="User")
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        update_instance(user, {"is_active": False})
        return response(status_code=status.HTTP_200_OK, detail="Account successfully deleted")


class MeView(APIView):

    @has_permission([filters.IS_AUTHENTICATED])
    def get(self, request):
        return response(status_code=status.HTTP_200_OK, instance=request.user, serializer=cs.UserSerializer)

