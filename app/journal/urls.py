from django.conf.urls import url
from . import views
from .views import JournalList

# TODO: Create views for urls
entry_urls = [
    url(r'^edit/(?P<id>[0-9]+)$', views.edit_entry),
    url(r'^create/$', views.create_entry, name="create_entry"),
    url(r'^delete/(?P<id>[0-9]+)$', views.create_entry),
    url(r'^$', JournalList.as_view())
]