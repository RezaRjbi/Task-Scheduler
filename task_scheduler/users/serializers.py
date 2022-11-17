from rest_framework import serializers
from .models import User


class RegisterUserSerializer(serializers.Serializer):
    username = serializers.CharField(source="User.username")
    password = serializers.CharField(source="User.password")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["user_permissions", "groups"]
        read_only_fields = ["last_login", "is_superuser", "is_staff", "is_active", "email", "phone", "date_joined"]
        extra_kwargs = {"password": {"write_only": True}}


class UpdateUserSerializer(serializers.Serializer):
    email = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(source="User.username")
    password = serializers.CharField(source="User.password")


class ChangeRoleSerializer(serializers.Serializer):
    is_staff = serializers.ChoiceField([True, False])


class ChangeActiveStatusSerializer(serializers.Serializer):
    is_active = serializers.ChoiceField([True, False])


class DeleteAccountSerializer(serializers.Serializer):
    is_active = serializers.ChoiceField([True])
