from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

from users.models import User
from users.serializers import UserSerializer


class UserManagementTestCase(TestCase):
    client_class = APIClient

    @classmethod
    def setUpTestData(cls):
        cls.user_url = reverse("users")

        User.objects.create(username="testUser", password="password")
        User.objects.create(username="testUser2", password="password")
        User.objects.create(username="testUser3", password="password")
        cls.admin_user = User.objects.create(username="testAdmin", password="password", is_staff=True)
        cls.superuser = User.objects.create_superuser(username="superUser", password="password")

    def setUp(self) -> None:
        self.admin_user_token = Token.objects.get_or_create(user=self.admin_user)[0].key
        self.superuser_token = Token.objects.get_or_create(user=self.superuser)[0].key

    def test_get_user_list(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_user_token)
        response = self.client.get(self.user_url)
        serializer = UserSerializer(User.objects.all(), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["instances"], serializer.data)
