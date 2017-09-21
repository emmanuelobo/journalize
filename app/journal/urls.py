from django.conf.urls import url

# TODO: Create views for urls
list_urls = [
    url(r'^edit/(?P<id>[0-9]+)$', None),
    url(r'^create/$', None),
    url(r'^delete/(?P<id>[0-9]+)$', None)
]