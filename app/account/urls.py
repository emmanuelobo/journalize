from django.conf.urls import url

from account import views

account_urls = [url(r"^$", views.profile, name="account")]
