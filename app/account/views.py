from django.shortcuts import render


def profile(request):
    data = {}
    return render(request, "account/profile.html", data)


def password_management(request):
    data = {}
    return render(request, "account/passwords.html", data)


def email_management(request):
    data = {}
    return render(request, "account/email.html", data)


def notifications(request):
    data = {}
    return render(request, "account/notifications.html", data)
