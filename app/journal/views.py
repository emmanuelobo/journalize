from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile, File
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from geopy import Nominatim

from .forms import JournalForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from .models import Journal, Tag


class JournalList(LoginRequiredMixin, ListView):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	context_object_name = "entries"
	model = Journal
	template_name = "subtemplate/journal_entries.html"

	def get_queryset(self):
		journals = Journal.objects.filter(writer=self.request.user, is_draft=False)
		return journals


class JournalDrafts(LoginRequiredMixin, ListView):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	model = Journal
	template_name = "subtemplate/drafts.html"

	def get_queryset(self):
		journals = Journal.objects.filter(writer=self.request.user, is_draft=True)
		return journals


class EditEntry(UpdateView):
	model = Journal
	template_name = 'subtemplate/edit_journal_entry.html'
	pk_url_kwarg = 'id'
	success_url = reverse_lazy('entries')
	form_class = JournalForm

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.writer = self.request.user
		self.object.image.save(name=form.cleaned_data['image'], content='media/BeStill.jpg')
		self.object.save()
		return super(EditEntry, self).form_valid(form)

	def form_invalid(self, form):
		print(form.errors)
		raise BaseException


class PublishEntry(ListView):
	model = Journal
	template_name = "subtemplate/drafts.html"

	def get_queryset(self):
		id = self.kwargs['id']
		published_entry = Journal.objects.get(id=id)
		published_entry.is_draft = False
		published_entry.save()
		journals = Journal.objects.filter(writer=self.request.user, is_draft=True)
		return journals

	def get(self, request, id, *args, **kwargs):
		published_entry = Journal.objects.get(id=id)
		published_entry.is_draft = False
		published_entry.save()
		return redirect('drafts')


class CreateEntry(LoginRequiredMixin, CreateView):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'
	model = Journal
	template_name = 'subtemplate/new_journal_entry.html'
	form_class = JournalForm

	def form_valid(self, form):
		journal = form.save(commit=False)
		journal.writer = self.request.user
		coordinates = form.cleaned_data['location']
		tags = form.cleaned_data['tags']
		locator = Nominatim()
		print(locator.reverse(coordinates).raw['address'])
		try:
			location = "{}, {}".format(locator.reverse(coordinates).raw['address']['city'],
									   locator.reverse(coordinates).raw['address']['state'])

		except KeyError:
			try:
				location = "{}, {}".format(locator.reverse(coordinates).raw['address']['town'],
										   locator.reverse(coordinates).raw['address']['state'])

			except KeyError:
				try:
					location = "{}, {}".format(locator.reverse(coordinates).raw['address']['village'],
											   locator.reverse(coordinates).raw['address']['state'])

				except KeyError:
					try:
						location = "{}, {}".format(locator.reverse(coordinates).raw['address']['locality'],
												   locator.reverse(coordinates).raw['address']['state'])

					except KeyError:
						location = "{}, {}".format(locator.reverse(coordinates).raw['address']['county'],
												   locator.reverse(coordinates).raw['address']['state'])

			if location != 'ERROR':
				journal.location = location

		journal.save()
		print("Tags: {}".format(tags))
		for tag in tags.split('|'):
			Tag.objects.create(name=tag, journal=journal)

		return HttpResponseRedirect(reverse('entries'))

	def form_invalid(self, form):
		print('Invalid Form')
		return HttpResponseRedirect(reverse('create_entry'))


class EntryView(DetailView):
	model = Journal
	context_object_name = 'entry'
	pk_url_kwarg = 'id'
	template_name = 'subtemplate/journal_entry.html'


def filter_journal_tags(request, tag):
	all_entries = Journal.objects.all()
	entries = []
	for entry in all_entries:
		if entry.filter_by_tag(tag) is not None:
			entries.append(entry)

	data = {'entries': entries, 'tag': tag}
	return render(request, 'subtemplate/filter_tags.html', data)


def delete_entry(request, id):
	Journal.objects.get(id=id).delete()
	return HttpResponseRedirect(reverse('entries'))
