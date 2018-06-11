from django.shortcuts import render
from .decorators import logged_in_redirect


@logged_in_redirect
def home(request):
    return render(request, "home.html", {})
