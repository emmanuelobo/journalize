import os
import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files import File
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from geopy import Nominatim

from journalize.settings import BASE_DIR, MEDIA_URL
from .forms import JournalForm
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from .models import Journal, Tag
from .utils import get_location

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-4s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.DEBUG)
logger = logging.getLogger('journalize')

class JournalList(LoginRequiredMixin, ListView):
	login_url = "/login/"
	redirect_field_name = "redirect_to"

	context_object_name = "entries"
	model = Journal
	template_name = "subtemplate/journal_entries.html"

	def get_queryset(self):
		journals = Journal.objects.filter(writer=self.request.user, is_draft=False)
		return journals


class JournalDrafts(LoginRequiredMixin, ListView):
	login_url = "/login/"
	redirect_field_name = "redirect_to"

	model = Journal
	template_name = "subtemplate/drafts.html"

	def get_queryset(self):
		journals = Journal.objects.filter(writer=self.request.user, is_draft=True)
		return journals


class EditEntry(UpdateView):
	model = Journal
	template_name = "subtemplate/edit_journal_entry.html"
	pk_url_kwarg = "id"
	success_url = reverse_lazy("entries")
	form_class = JournalForm

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.writer = self.request.user
		# self.object.image.save(name=form.cleaned_data['image'], content='media/BeStill.jpg')
		# form.clean()
		# self.object.image.save(form.cleaned_data['image'], File(open(os.path.join(BASE_DIR, 'media') + '\\' + 'BeStill.jpg', 'rb')))
		# print(form.cleaned_data['image'])
		# self.object.image.path = '/media/BoardWalk.jpeg'
		self.object.save()
		return super(EditEntry, self).form_valid(form)

	def form_invalid(self, form):
		print(form.errors)
		raise BaseException


class PublishEntry(ListView):
	model = Journal
	template_name = "subtemplate/drafts.html"

	def get_queryset(self):
		id = self.kwargs["id"]
		published_entry = Journal.objects.get(id=id)
		published_entry.is_draft = False
		published_entry.save()
		journals = Journal.objects.filter(writer=self.request.user, is_draft=True)
		return journals

	def get(self, request, id, *args, **kwargs):
		published_entry = Journal.objects.get(id=id)
		published_entry.is_draft = False
		published_entry.save()
		return redirect("drafts")


class CreateEntry(LoginRequiredMixin, CreateView):
	login_url = "/login/"
	redirect_field_name = "redirect_to"
	model = Journal
	template_name = "subtemplate/new_journal_entry.html"
	form_class = JournalForm

	def form_valid(self, form):
		logger.info("inside form_valid() method")
		journal = form.save(commit=False)
		journal.writer = self.request.user
		latitude, longitude = form.cleaned_data["location"].split(',')
		tags = form.cleaned_data["tags"]
		location = get_location(latitude, longitude)
		journal.location = location

		journal.save()
		for tag in tags.split("|"):
			if len(tag.split()) == 0:
				pass
			else:
				Tag.objects.create(name=tag, journal=journal)

		return HttpResponseRedirect(reverse("entries"))

	def form_invalid(self, form):
		print("Invalid Form")
		return HttpResponseRedirect(reverse("create_entry"))


class EntryView(DetailView):
	model = Journal
	context_object_name = "entry"
	pk_url_kwarg = "id"
	template_name = "subtemplate/journal_entry.html"


def filter_journal_tags(request, tag):
	all_entries = Journal.objects.all()
	entries = []
	for entry in all_entries:
		if entry.filter_by_tag(tag) is not None:
			entries.append(entry)

	data = {"entries": entries, "tag": tag}
	return render(request, "subtemplate/filter_tags.html", data)


def delete_entry(request, id):
	Journal.objects.get(id=id).delete()
	return HttpResponseRedirect(reverse("entries"))
