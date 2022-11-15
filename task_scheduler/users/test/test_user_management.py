from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User
from users.serializers import UserSerializer


class UserManagementTestCase(TestCase):
    client_class = APIClient

    @classmethod
    def setUpTestData(cls):
        cls.user_url = reverse("users")

    def test_user_register(self):
        response = self.client.post(self.user_url, data={"username": "testUser", "password": "password"})
        user = User.objects.get(username="testUser")
        serializer = UserSerializer(user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["instances"], serializer.data)


