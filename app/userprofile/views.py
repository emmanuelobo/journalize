from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from journalize.decorators import logged_in_redirect

from .forms import UserLoginForm, UserRegistrationForm


@logged_in_redirect
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print("username: {} | password: {}".format(username, password))
        user = authenticate(request, username=username, password=password)
        print(user)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/entry/")

    print("Login was unsuccessful")
    form = UserLoginForm()
    temp_tags = {"form": form}
    return render(request, "subtemplate/login.html", temp_tags)


@logged_in_redirect
def register(request):
    form = UserRegistrationForm()
    temp_tags = {"form": form}
    return render(request, "subtemplate/register.html", temp_tags)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")
