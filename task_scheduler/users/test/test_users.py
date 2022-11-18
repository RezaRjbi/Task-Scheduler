from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from users.models import User
from users.serializers import UserSerializer


class UserTestCase(TestCase):
    client_class = APIClient

    @classmethod
    def setUpTestData(cls):
        cls.user_url = reverse("users")
        cls.admin_user = User.objects.create(username="testAdmin", password="password", is_staff=True)

    def setUp(self):
        self.sample_user = User.objects.create_user(username="testUser", password="password")
        self.sample_user_token = Token.objects.get_or_create(user=self.sample_user)[0].key
        self.admin_user_token = Token.objects.get_or_create(user=self.admin_user)[0].key

    def test_user_register(self):
        response = self.client.post(self.user_url, data={"username": "testUser2", "password": "password"})
        user = User.objects.get(username="testUser2")
        serializer = UserSerializer(user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["instances"], serializer.data)

    def test_identical_username_registration(self):
        response = self.client.post(self.user_url, data={"username": "testUser", "password": "password2"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_user_token)
        id = self.sample_user.id
        response = self.client.get(f"{self.user_url}{id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = UserSerializer(self.sample_user)
        self.assertEqual(response.json()["instances"], serializer.data)

    def test_retrieve_user_by_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.sample_user_token)
        id = self.sample_user.id
        response = self.client.get(f"{self.user_url}{id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = UserSerializer(self.sample_user)
        self.assertEqual(response.json()["instances"], serializer.data)

    def test_retrieve_user_by_others(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.sample_user_token)
        response = self.client.get(f"{self.user_url}{self.admin_user.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.sample_user_token)
        id = self.sample_user.id
        response = self.client.put(f"{self.user_url}{id}/", {"first_name": "firstname", "email": "a@aiij.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_user = UserSerializer(User.objects.get(pk=id))
        self.assertEqual(response.json()["instances"], updated_user.data)

    def test_delete_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_user_token)
        id = self.sample_user.id
        response = self.client.delete(f"{self.user_url}{id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaisesMessage(User.DoesNotExist, "User matching query does not exist."):
            User.objects.get(username=self.sample_user.username)

    def test_login(self):
        # todo
        ...

    def test_logout(self):
        # todo
        ...

    def test_delete_account(self):
        # todo
        ...
