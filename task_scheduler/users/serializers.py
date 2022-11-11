from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ["user_permissions", "groups"]
        read_only_fields = ["last_login", "is_superuser", "is_staff", "is_active", "email", "phone", "date_joined"]
        extra_kwargs = {"password": {"write_only": True}}


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(source="User.username")
    password = serializers.CharField(source="User.password")
