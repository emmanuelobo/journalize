from django.test import TestCase
from django.urls import reverse


class AccountTests(TestCase):
	def test_navigate_to_profile_page(self):
		url = reverse('account')
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)
		self.assertContains(response, "<title>My Profile</title>")
