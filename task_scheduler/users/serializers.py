from rest_framework import serializers
from pydantic import BaseModel, Field, validator
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["user_permissions", "groups"]

        extra_kwargs = {"password": {"write_only": True}}


class LoginSerializer(BaseModel):
    username: str = Field(max_length=128)
    password: str

