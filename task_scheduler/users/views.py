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
        serializer = UserSerializer(users, many=True)
        return response(instance=serializer.data, total=users.count())

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return response(UserSerializer(user).data)
        return response(errors=serializer.errors)


class LoginView(APIView):

    def post(self, request, format=None):

        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return response(errors=serializer.errors)
        data = serializer.data
        try:
            User.objects.get(username=data["username"])
        except User.DoesNotExist:
            return response(errors="user not found", status_code=status.HTTP_404_NOT_FOUND)
        user = authenticate(username=data["username"], password=data["password"])
        if not user:
            return response(errors="Wrong credentials")
        login(request, user)
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
        return response(
            data=f"{user.username} logged in successfully",
            status_code=status.HTTP_200_OK, token=token.key
        )


class LogoutView(APIView):

    def post(self, request, format=None):
        logout(request)
        return response(data="Successfully logged out")
