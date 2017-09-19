from django.shortcuts import render

# Create your views here.
from .forms import UserLoginForm


def login(request):
    form = UserLoginForm()
    temp_tags = {"form": form}
    return render(request, 'login.html', temp_tags)