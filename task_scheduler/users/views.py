from rest_framework.views import APIView, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate, login, logout

from .models import User
from .serializers import UserSerializer, LoginSerializer

from .permissions import IsAdminOrNewUser

from utils.general import response


class ListCreateUserView(APIView):
    permission_classes = [IsAdminOrNewUser]

    def get(self, request):
        users = User.objects.all()
        return response(instance=users, serializer=UserSerializer, many=True, total=users.count())

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return response(instance=user, status_code=status.HTTP_201_CREATED, serializer=UserSerializer)
        return response(errors=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)


class RetrieveUpdateDestroyUserView(APIView):
    def get(self, request):
        ...
        # todo

    def put(self, request):
        ...
        #  todo

    def delete(self, request):
        ...
        #  todo


class LoginView(APIView):

    def post(self, request, format=None):

        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return response(errors=serializer.errors)
        data = serializer.data
        try:
            User.objects.get(username=data["username"])
        except User.DoesNotExist as e:
            return response(data="user not found", errors=str(e), status_code=status.HTTP_404_NOT_FOUND)
        user = authenticate(username=data["username"], password=data["password"])
        if not user:
            return response(
                data="provided username and password dont match",
                errors="wrong_credentials", status_code=status.HTTP_401_UNAUTHORIZED
            )

        token = Token.objects.get_or_create(user=user)
        return response(
            data=f"{user.username} logged in successfully",
            status_code=status.HTTP_200_OK, token=token[0].key
        )


class LogoutView(APIView):

    def post(self, request, format=None):
        request.user.auth_token.delete()
        return response(data="Successfully logged out", status_code=status.HTTP_200_OK)


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
