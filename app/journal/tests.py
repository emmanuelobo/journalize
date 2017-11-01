from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from journal.forms import JournalForm


class JournalTestsSetUp(TestCase):
	def setUp(self):
		self.credentials = {
			'username': 'testuser',
			'password': 'secret',
			'email': 'someone@email.com'}
		User.objects.create_user(**self.credentials)

		# Login to the app
		url = reverse('login')
		self.client.post(url, data=self.credentials)


class JournalTests(JournalTestsSetUp, TestCase):
	def test_navigate_to_create_entry_url(self):
		url = reverse('create_entry')
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)

	def test_contains_journal_form(self):
		url = reverse('create_entry')
		response = self.client.get(url)
		form = response.context.get('form')
		self.assertIsInstance(form, JournalForm)
		self.assertFalse(form.is_bound)

	def test_journal_creation_form_inputs(self):
		url = reverse('create_entry')
		response = self.client.get(url)
		self.assertContains(response, '<input', 6)
		self.assertContains(response, 'id="id_title"', 1)
		self.assertContains(response, 'id="id_text"', 1)
		self.assertContains(response, 'id="id_image"', 1)
		self.assertContains(response, 'id="id_location"', 1)
		self.assertContains(response, 'id="id_tags"', 1)
		self.assertContains(response, 'required', 2)


	def test_invalid_form_post_redirects(self):
		url = reverse('create_entry')
		data = {'title': '', 'text': '', 'image': '', 'location': ''}
		response = self.client.post(url, data)
		self.assertRedirects(response, url)

	def test_successful_form_post_redirect(self):
		url, create_url = reverse('entries'), reverse('create_entry')
		data = {'title': 'Test Title', 'text': 'testing...', 'image': '', 'location': '36.23434, 53.44343', 'tags': ''}
		response = self.client.post(create_url, data)
		self.assertRedirects(response, url)
		response = self.client.get(url)

		# Test Entry Properties after Published
		self.assertContains(response, data['title'])
		self.assertContains(response, data['text'])
		self.assertContains(response, 'min read', 1)

	def test_save_entry_as_draft(self):
		pass




