from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from users.models import User
from users.serializers import UserSerializer


class UserTestCase(TestCase):
    client_class = APIClient

    @classmethod
    def setUpTestData(cls):
        cls.user_url = reverse("users")

    def setUp(self):
        self.sample_user = User.objects.create(username="testUser", password="password")
        self.sample_user.refresh_from_db()

    def test_identical_username_registration(self):
        response = self.client.post(self.user_url, data={"username": "testUser", "password": "password2"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user(self):
        response = self.client.get(f"{self.user_url}1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = UserSerializer(self.sample_user)
        self.assertEqual(response.json()["instances"], serializer.data)

    def test_update_user(self):
        response = self.client.put(f"{self.user_url}1/", {"phone": "09355556589", "email": "a@aiij.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_user = UserSerializer(User.objects.get(pk=1))
        self.assertEqual(response.json()["instances"], updated_user.data)

    def test_delete_user(self):
        response = self.client.delete(f"{self.user_url}1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaisesMessage(User.DoesNotExist, "User matching query does not exist."):
            User.objects.get(pk=1)
