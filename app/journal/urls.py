from django.conf.urls import url
from . import views
from .views import JournalList, JournalDrafts, PublishEntry, filter_journal_tags

entry_urls = [
    url(r"tags/(?P<tag>[a-zA-Z0-9_ -]+)$", filter_journal_tags, name="filter_tags"),
    url(r"(?P<id>[0-9]+)$", views.EntryView.as_view(), name="view_entry"),
    url(r"^(?P<id>[0-9]+)/edit$", views.EditEntry.as_view(), name="edit_entry"),
    url(r"^create/$", views.CreateEntry.as_view(), name="create_entry"),
    url(r"^(?P<id>[0-9]+)/delete$", views.delete_entry, name="delete_entry"),
    url(r"^draft/$", JournalDrafts.as_view(), name="drafts"),
    url(r"^draft/(?P<id>[0-9]+)/publish$", PublishEntry.as_view(), name="publish_draft"),
    url(r"^$", JournalList.as_view(), name="entries"),
]
