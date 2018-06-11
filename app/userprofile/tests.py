from django.contrib.auth.models import User
from django.http import response
from django.test import TestCase
from django.urls import reverse


class UserTests(TestCase):
    def setUp(self):
        self.credentials = {"username": "testuser", "password": "secret"}

        User.objects.create_user(**self.credentials)

        # Login to the app
        url = reverse("login")
        response = self.client.post(url, data=self.credentials)

    def test_navigate_to_entries(self):
        url = reverse("entries")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_user_logout(self):
        url = reverse("logout")
        response = self.client.get(url)
        self.assertTrue(response.context["user"].is_active)
