from django.shortcuts import render


from .forms import UserLoginForm, UserRegistrationForm


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("Attempted Login")
        print("{} : {}".format(username,password))

    form = UserLoginForm()
    temp_tags = {"form": form}
    return render(request, 'subtemplate/login.html', temp_tags)

def register(request):
    form = UserRegistrationForm()
    temp_tags = {"form": form}
    return render(request, 'subtemplate/register.html', temp_tags)