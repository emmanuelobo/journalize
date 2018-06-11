from django.conf.urls import url


user_urls = [
    url(r"^edit/(?P<id>[0-9]+)$", None, name="edit_profile"),
    url(r"^delete/(?P<id>[0-9]+)$", None, name="delete_profile"),
]
