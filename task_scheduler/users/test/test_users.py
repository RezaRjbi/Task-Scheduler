from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


class UserTestCase(TestCase):

    def test_identical_username_registration(self):
        client = APIClient()
        url = reverse("users")
        client.post(url, data={"username": "testUser", "password": "password"})
        response = client.post(url, data={"username": "testUser", "password": "password2"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
