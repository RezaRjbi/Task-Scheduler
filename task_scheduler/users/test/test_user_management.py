from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User
from users.serializers import UserSerializer


class UserManagementTestCase(TestCase):

    def test_user_register(self):
        client = APIClient()
        url = reverse("users")
        response = client.post(url, data={"username": "testUser", "password": "password"})
        user = User.objects.get(username="testUser")
        serializer = UserSerializer(user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["instances"], serializer.data)


