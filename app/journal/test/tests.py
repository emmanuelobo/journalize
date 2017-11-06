from django.contrib.auth.models import User
from django.test import TestCase, LiveServerTestCase
from django.urls import reverse
from journal.forms import JournalForm
from journal.models import Journal
from journal.models import Tag


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

	def create_entry(self):
		create_url = reverse('create_entry')
		data = {'title': 'Test Title', 'text': 'testing...', 'image': '', 'location': '36.23434, 53.44343', 'tags': 'test'}
		self.client.post(create_url, data)

	def get_single_tag(self):
		self.create_entry()
		tag = Tag.objects.get(id=1)
		return tag.name


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

		# Test Entry Fields after Published
		self.assertContains(response, data['title'])
		self.assertContains(response, data['text'])
		self.assertContains(response, 'min read', 1)

	def test_journal_list_view(self):
		super().create_entry()
		url = reverse('entries')
		response = self.client.get(url)
		entries = response.context['entries']
		self.assertEqual(len(entries), 1)

	def test_preview_journal_entry(self):
		super().create_entry()
		url = reverse('view_entry', kwargs={'id': 1})
		response = self.client.get(url)
		entry = response.context['entry']
		self.assertEquals(response.status_code, 200)
		self.assertIsInstance(entry, Journal)
		self.assertContains(response, entry.title)
		self.assertContains(response, entry.text)

	def test_navigate_to_drafts(self):
		url = reverse('drafts')
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)

	def test_empty_drafts_list(self):
		url = reverse('drafts')
		response = self.client.get(url)
		drafts = response.context['object_list']
		self.assertEquals(len(drafts), 0)
		self.assertContains(response, 'You Don\'t Have Any Drafts At The Moment')

	def test_no_entries(self):
		url = reverse('entries')
		response = self.client.get(url)
		entries = response.context['entries']
		self.assertEquals(len(entries), 0)
		self.assertContains(response, 'No Journal Entries Written Yet ☹')
		self.assertContains(response, 'Get started writing awesome Journal Entries today!')

	def test_edit_journal_entry(self):
		super().create_entry()
		url = reverse('edit_entry', kwargs={'id': 1})
		entry = Journal.objects.get(id=1)
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)
		form = response.context['form']
		self.assertIsNotNone(form)
		self.assertIsInstance(form, JournalForm)
		self.assertFalse(form.is_bound)
		self.assertTrue(form.is_valid)
		self.assertContains(response, entry.title)
		self.assertContains(response, entry.text)

	def test_save_entry_as_draft(self):
		pass

	def test_delete_draft_entry(self):
		pass

	def test_edit_draft_entry(self):
		pass

	def test_delete_journal_entry(self):
		pass

	def test_filter_entries_by_tag(self):
		tag = super().get_single_tag()
		url = reverse('filter_tags', kwargs={'tag': tag})
		response = self.client.get(url)
		self.assertContains(response, 'Filter Tags: {}'.format(tag))
		entries = response.context['entries']
		print(response.context)
		self.assertGreater(len(entries), 0)

	def test_no_results_for_filtered_tag(self):
		url = reverse('filter_tags', kwargs={'tag': 'random tag'})
		response = self.client.get(url)
		entries = response.context['entries']
		self.assertContains(response, 'No Results Found')
		self.assertContains(response, 'Return Home')
		self.assertEquals(len(entries), 0)


